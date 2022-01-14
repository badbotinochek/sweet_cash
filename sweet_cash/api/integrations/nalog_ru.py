import requests
import logging

from api.api import check_phone_format
from config import Config
from api.services.users.get_user import GetUser
from api.services.nalog_ru_sessions.create_or_update_nalog_ru_session import CreateOrUpdateNalogRuSession
from api.services.nalog_ru_sessions.get_nalog_ru_session import GetNalogRuSession
import api.errors as error

logger = logging.getLogger(name="nalog_ru")


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

    def check_response(self, response, *args):
        if response.status_code in self.SUCCESS_CODE:
            logger.error(f'NalogRu API error. Response {response}')
            raise error.APIError(f'NalogRu API error {response.status_code} {response.text}')

        for arg in args:
            if arg not in response.json():
                logger.error(f'NalogRu API error. {arg} not in response. Response {response}')
                raise error.APIError(f'NalogRu API error {response.status_code} {response.text}')

    def send_otp_sms(self, user_id: int, get_user=GetUser()):
        """
        Send SMS with otp
        """
        user = get_user(user_id=user_id)

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

        self.check_response(response)

    def verify_otp(self, user_id: int, otp: str,
                   get_user=GetUser(),
                   create_or_update_nalog_ru_session=CreateOrUpdateNalogRuSession()):
        """
        Verify otp from SMS
        """
        user = get_user(user_id=user_id)

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

        self.check_response(response, "sessionId", "refresh_token")

        session_id = response.json()["sessionId"]
        refresh_token = response.json()["refresh_token"]

        create_or_update_nalog_ru_session(user_id=user_id,
                                          session_id=session_id,
                                          refresh_token=refresh_token)

        logger.info(f'User {user_id} verified otp for phone {phone}')

    def refresh_token(self, user_id: int,
                      get_nalog_ru_session=GetNalogRuSession(),
                      create_or_update_nalog_ru_session=CreateOrUpdateNalogRuSession()) -> str:

        session = get_nalog_ru_session(user_id=user_id)

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

        self.check_response(response, "sessionId", "refresh_token")

        session_id = response.json()["sessionId"]
        refresh_token = response.json()["refresh_token"]

        create_or_update_nalog_ru_session(user_id=user_id,
                                          session_id=session_id,
                                          refresh_token=refresh_token)

        logger.info(f'Updated session id and refresh token for user {user_id}')

        return session_id

    def __get_ticket_id(self, user_id: int, session_id: int, qr: str) -> str:
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

        self.check_response(response, "id")

        ticket_id = response.json()["id"]

        logger.info(f'Got ticket id {ticket_id} for user {user_id}')

        return ticket_id

    def get_ticket(self, user_id: int, qr: str, get_nalog_ru_session=GetNalogRuSession()):
        """
        Get JSON ticket
        :param user_id: user id
        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :param get_nalog_ru_session: class for getting NalogRu session
        :return: JSON ticket
        """

        session = get_nalog_ru_session(user_id=user_id)

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

        self.check_response(response, "id")

        logger.info(f'Got ticket {ticket_id} for user {user_id}')

        return ticket_id, response.json()
