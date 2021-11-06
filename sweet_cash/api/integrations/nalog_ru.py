from datetime import datetime
import requests
import logging

from api.api import check_phone_format
from sweet_cash.config import Config
from api.models.users import UserModel
from api.models.external_session import NalogRuSessionModel
import api.errors as error
from db import db

logger = logging.getLogger(name="nalog_ru")


def create_or_update_session(user_id: str, session_id: str, refresh_token: str):
    external_session = NalogRuSessionModel.get_by_user(user_id=user_id)

    if external_session is None:
        external_session = NalogRuSessionModel(user_id=user_id,
                                               session_id=session_id,
                                               refresh_token=refresh_token)
        db.session.add(external_session)

        logger.info(f'Created new NalogRuSession for user {user_id}')

    else:
        external_session.session_id = session_id
        external_session.refresh_token = refresh_token
        external_session.updated_at = datetime.utcnow().isoformat()

        logger.info(f'Updated NalogRuSession for user {user_id}')

    db.session.commit()


class NalogRuApi:
    HOST = Config.NALOG_RU_HOST
    CLIENT_SECRET = Config.NALOG_RU_CLIENT_SECRET
    OS = Config.NALOG_RU_OS
    DEVICE_OS = Config.NALOG_RU_DEVICE_OS
    DEVICE_ID = Config.NALOG_RU_DEVICE_ID

    def send_otp_sms(self, user_id: str):
        """
        Send SMS with otp
        """
        user = UserModel.get(user_id=user_id)

        phone = user.get_phone()

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

        return response.text, response.status_code

    def verify_otp(self, user_id: str, otp: str):
        """
        Verify otp from SMS
        """
        user = UserModel.get(user_id=user_id)

        phone = user.get_phone()

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

        if 'application/json' not in response.headers.get('content-Type') or \
                'sessionId' not in response.json() or "refresh_token" not in response.json():
            logger.error(f'Error verification otp {otp} for phone {phone}. Response from NalogRu {response}')
            raise error.APIError(response.text, response.status_code)

        session_id = response.json()["sessionId"]
        refresh_token = response.json()["refresh_token"]

        create_or_update_session(user_id=user_id, session_id=session_id, refresh_token=refresh_token)

        logger.info(f'User {user_id} verified otp for phone {phone}')

    def refresh_token(self, user_id: str) -> str:

        session = NalogRuSessionModel.get_by_user(user_id=user_id)

        if session is None:
            raise error.APIAuthError('User is not authorized in NalogRu Api')

        refresh_token = session.get_refresh_token()

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

        if 'application/json' not in response.headers.get('content-Type') or \
                'sessionId' not in response.json() or "refresh_token" not in response.json():
            logger.error(f'Error refresh token. Response from NalogRu {response}')
            raise error.APIError(response.text, response.status_code)

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

        if 'application/json' not in response.headers.get('content-Type') or 'id' not in response.json():
            logger.error(f'Error getting ticket id. Response from NalogRu {response}')
            raise error.APIError(response.text, response.status_code)

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

        session = NalogRuSessionModel.get_by_user(user_id=user_id)

        if session is None:
            raise error.APIAuthError('User is not authorized in NalogRu Api')

        session_id = session.get_session_id()

        ticket_id = self.__get_ticket_id(user_id=user_id, session_id=session_id, qr=qr)

        url = f'{self.HOST}/v2/tickets/{ticket_id}'

        headers = {
            'sessionId': session_id,
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if 'application/json' not in response.headers.get('content-Type'):
            logger.error(f'Error getting ticket. Response from NalogRu {response}')
            raise error.APIError(response.text, response.status_code)

        logger.info(f'Got ticket {ticket_id} for user {user_id}')

        return ticket_id, response.json()

# class NalogRu:
#     HOST = Config.NALOG_RU_HOST
#     CLIENT_SECRET = Config.NALOG_RU_CLIENT_SECRET
#     OS = Config.NALOG_RU_OS
#
#     def __init__(self, session_id=None, refresh_token=None):
#         self.__phone = None
#         self.__code = None
#         self.__session_id = session_id
#         self.__refresh_token = refresh_token
#         if session_id is None:
#             self.set_session_id()
#
#     def set_session_id(self) -> None:
#         """
#         Authorization using phone and SMS code
#         """
#         self.__phone = str(input('Input phone in +70000000000 format: '))
#
#         url = f'{self.HOST}/v2/auth/phone/request'
#
#         payload = {
#             'phone': self.__phone,
#             'client_secret': self.CLIENT_SECRET,
#             'os': self.OS
#         }
#
#         resp = requests.post(url, json=payload)
#
#         self.__code = input('Input code from SMS: ')
#
#         url = f'{self.HOST}/v2/auth/phone/verify'
#
#         payload = {
#             'phone': self.__phone,
#             'client_secret': self.CLIENT_SECRET,
#             'code': self.__code,
#             "os": self.OS
#         }
#
#         resp = requests.post(url, json=payload)
#
#         self.__session_id = resp.json()['sessionId']
#         self.__refresh_token = resp.json()['refresh_token']
#
#         print(resp.json()['sessionId'])
#         print(resp.json()['refresh_token'])
#
#     def refresh_token_function(self) -> None:
#         url = f'{self.HOST}/v2/mobile/users/refresh'
#
#         payload = {
#             'refresh_token': self.__refresh_token,
#             'client_secret': self.CLIENT_SECRET
#         }
#
#         resp = requests.post(url, json=payload)
#
#         self.__session_id = resp.json()['sessionId']
#         self.__refresh_token = resp.json()['refresh_token']
#
#     def _get_ticket_id(self, qr: str) -> str:
#         """
#         Get ticker id by info from qr code
#         :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
#         :return: Ticket id. Example "5f3bc6b953d5cb4f4e43a06c"
#         """
#         url = f'{self.HOST}/v2/ticket'
#
#         payload = {
#             'qr': qr
#         }
#         headers = {
#             'sessionId': self.__session_id
#         }
#
#         resp = requests.post(url, json=payload, headers=headers)
#
#         return resp.json()["id"]
#
#     def get_ticket(self, qr: str) -> dict:
#         """
#         Get JSON ticket
#         :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
#         :return: JSON ticket
#         """
#         ticket_id = self._get_ticket_id(qr)
#
#         url = f'{self.HOST}/v2/tickets/{ticket_id}'
#
#         headers = {
#             'sessionId': self.__session_id,
#             'Content-Type': 'application/json'
#         }
#
#         resp = requests.get(url, headers=headers)
#
#         return resp.json()


# if __name__ == '__main__':
#     client = NalogRu(session_id=SESSION_ID, refresh_token=REFRESH_TOKEN)
#     qr_code = "t=20200709T2008&s=7273.00&fn=9282440300688488&i=14186&fp=1460060363&n=1"
#     ticket = client.get_ticket(qr_code)
#     print(json.dumps(ticket, indent=4, ensure_ascii=False))
#
#     # client.refresh_token_function()
#     # qr_code = "t=20200924T1837&s=349.93&fn=9282440300682838&i=46534&fp=1273019065&n=1"
#     # ticket = client.get_ticket(qr_code)
#     # print(json.dumps(ticket, indent=4, ensure_ascii=False))
