import requests
import logging

from api.api import check_phone_format
from config import Config
from api.services.user import User
from api.services.nalog_ru_session import NalogRuSession
import api.errors as error

logger = logging.getLogger(name="nalog_ru")


def create_or_update_session(user_id: str, session_id: str, refresh_token: str):
    NalogRuSession(user_id=user_id,
                   session_id=session_id,
                   refresh_token=refresh_token).update()


# Реализация синглтона через метакласс
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NalogRuApi(metaclass=Singleton):
    HOST = Config.NALOG_RU_HOST
    CLIENT_SECRET = Config.NALOG_RU_CLIENT_SECRET
    OS = Config.NALOG_RU_OS
    DEVICE_OS = Config.NALOG_RU_DEVICE_OS
    DEVICE_ID = Config.NALOG_RU_DEVICE_ID
    SUCCESS_CODE = [200, 204]

    def send_otp_sms(self, user_id: str):
        """
        Send SMS with otp
        """
        user = User(user_id=user_id).get()

        if user is None:
            raise error.APIValueNotFound('User not found')

        phone = user.phone

        if not check_phone_format(phone):
            raise error.APIParamError('Invalid phone format')

        url = f'{self.HOST}/v2/auth/phone/request'

        payload = {
            'phone': phone,
            'client_secret': self.CLIENT_SECRET,
            'os': self.OS
        }

        response = requests.post(url, json=payload)

        logger.info(f'User {user_id} is trying to send otp SMS')

        if response.status_code in self.SUCCESS_CODE:
            logger.error(f'Error sending sms. Response from NalogRu {response}')
            raise error.APIError(f'NalogRu API error {response.status_code} {response.text}')

    def verify_otp(self, user_id: str, otp: str):
        """
        Verify otp from SMS
        """
        user = User(user_id=user_id).get()

        if user is None:
            raise error.APIValueNotFound('User not found')

        phone = user.phone

        if not check_phone_format(phone):
            raise error.APIError('Invalid phone format')

        url = f'{self.HOST}/v2/auth/phone/verify'

        payload = {
            'phone': phone,
            'client_secret': self.CLIENT_SECRET,
            'code': otp,
            "os": self.OS
        }

        response = requests.post(url, json=payload)

        if response.status_code in self.SUCCESS_CODE or \
                'sessionId' not in response.json() or "refresh_token" not in response.json():
            logger.error(f'Error verification otp {otp} for phone {phone}. Response from NalogRu {response}')
            raise error.APIError(f'NalogRu API error {response.status_code} {response.text}')

        session_id = response.json()["sessionId"]
        refresh_token = response.json()["refresh_token"]

        create_or_update_session(user_id=user_id, session_id=session_id, refresh_token=refresh_token)

        logger.info(f'User {user_id} verified otp for phone {phone}')

    def refresh_token(self, user_id: str) -> str:

        session = NalogRuSession(user_id=user_id).get()

        if session is None:
            raise error.APIAuthError('User is not authorized in NalogRu Api')

        refresh_token = session.refresh_token

        url = f'{self.HOST}/v2/mobile/users/refresh'

        payload = {
            'refresh_token': refresh_token,
            'client_secret': self.CLIENT_SECRET
        }

        headers = {
            'Device-OS': self.DEVICE_OS,
            'Device-Id': self.DEVICE_ID
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code in self.SUCCESS_CODE or \
                'sessionId' not in response.json() or "refresh_token" not in response.json():
            logger.error(f'Error refresh token. Response from NalogRu {response}')
            raise error.APIError(f'NalogRu API error {response.status_code} {response.text}')

        session_id = response.json()["sessionId"]
        refresh_token = response.json()["refresh_token"]

        create_or_update_session(user_id=user_id, session_id=session_id, refresh_token=refresh_token)

        logger.info(f'Updated session id and refresh token for user {user_id}')

        return session_id

    def __get_ticket_id(self, user_id: str, session_id: str, qr: str) -> str:
        """
        Get ticker id by info from qr code
        :param session_id: session id for auth
        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :return: Ticket id. Example "5f3bc6b953d5cb4f4e43a06c"
        """
        url = f'{self.HOST}/v2/ticket'

        payload = {
            'qr': qr
        }

        headers = {
            'sessionId': session_id
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 401:
            new_session_id = self.refresh_token(user_id=user_id)

            headers = {
                'sessionId': new_session_id
            }

            response = requests.post(url, json=payload, headers=headers)

        if response.status_code in self.SUCCESS_CODE or 'id' not in response.json():
            logger.error(f'Error getting ticket id. Response from NalogRu {response}')
            raise error.APIError(f'NalogRu API error {response.status_code} {response.text}')

        ticket_id = response.json()["id"]

        logger.info(f'Got ticket id {ticket_id} for user {user_id}')

        return ticket_id

    def get_ticket(self, user_id: str, qr: str):
        """
        Get JSON ticket
        :param user_id: user id
        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :return: JSON ticket
        """

        session = NalogRuSession(user_id=user_id).get()

        if session is None:
            raise error.APIAuthError('User is not authorized in NalogRu Api')

        session_id = session.session_id

        ticket_id = self.__get_ticket_id(user_id=user_id, session_id=session_id, qr=qr)

        url = f'{self.HOST}/v2/tickets/{ticket_id}'

        headers = {
            'sessionId': session_id,
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code in self.SUCCESS_CODE:
            logger.error(f'Error getting ticket. Response from NalogRu {response}')
            raise error.APIError(f'NalogRu API error {response.status_code} {response.text}')

        logger.info(f'Got ticket {ticket_id} for user {user_id}')

        return ticket_id, response.json()
