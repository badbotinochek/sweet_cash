import requests
import logging

from sweet_cash.config import Config
from sweet_cash.api.services.nalog_ru.create_or_update_nalog_ru_session import CreateOrUpdateNalogRuSession
import sweet_cash.api.errors as error

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
        if response.status_code not in self.SUCCESS_CODE:
            logger.error(f'NalogRu API error. Response {response}')
            raise error.APIError(f'NalogRu API error {response.status_code} {response.text}')

        for arg in args:
            if arg not in response.json():
                logger.error(f'NalogRu API error. {arg} not in response. Response {response}')
                raise error.APIError(f'NalogRu API error {response.status_code} {response.text}')

    def send_otp_sms(self, phone: str):
        """
        Send SMS with otp
        """
        url = f'{self.HOST}/v2/auth/phone/request'

        payload = {
            'phone': phone,
            'client_secret': self.CLIENT_SECRET,
            'os': self.OS
        }

        response = requests.post(url, json=payload)

        self.check_response(response)

    def verify_otp(self, phone: str, otp: str):
        """
        Verify otp from SMS
        """
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

        return session_id, refresh_token

    def __get_new_session_id(self, user_id: int, refresh_token: str,
                             create_or_update_nalog_ru_session=CreateOrUpdateNalogRuSession()) -> str:
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

        return session_id

    def __get_ticket_id(self, user_id: int, session_id: str, refresh_token: str, qr: str) -> str:
        """
        Get ticker id by info from qr code
        :param user_id: user id
        :param session_id: session id for  auth in nalog ru
        :param refresh_token: refresh_token for auth in nalog ru
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
            new_session_id = self.__get_new_session_id(user_id=user_id, refresh_token=refresh_token)

            headers = {
                'sessionId': new_session_id
            }

            response = requests.post(url, json=payload, headers=headers)

        self.check_response(response, "id")

        ticket_id = response.json()["id"]

        return ticket_id

    def get_ticket(self, user_id: int, session_id: str, refresh_token: str, qr: str):
        """
        Get JSON ticket
        :param user_id: user id
        :param session_id: session_id for nalog ru
        :param refresh_token: refresh_token id for nalog ru
        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :return: JSON ticket
        """

        ticket_id = self.__get_ticket_id(user_id=user_id, session_id=session_id, refresh_token=refresh_token, qr=qr)

        url = f'{self.HOST}/v2/tickets/{ticket_id}'

        headers = {
            'sessionId': session_id,
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)

        self.check_response(response, "id")

        return ticket_id, response.json()
