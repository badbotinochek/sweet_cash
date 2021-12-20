from flask import Blueprint
import logging

from api.api import SuccessResponse, jsonbody, features, query_params
from api.services.users.register_user import RegisterUser
from api.services.users.login_user import LoginUser
from api.services.users.get_access_token import GetAccessToken
from api.services.users.confirm_user import ConfirmUser
from api.services.email_sending.send_email import SendEmail

logger = logging.getLogger(name="auth")

auth_api = Blueprint('login', __name__)


@auth_api.route('/api/v1/register', methods=['POST'])
@jsonbody(name=features(type=str, required=True),
          email=features(type=str, required=True),
          phone=features(type=str, required=True),
          password=features(type=str, required=True))
def register(name: str,
             email: str,
             phone: str,
             password: str,
             register_user=RegisterUser()):
    return SuccessResponse(register_user(name=name,
                                         email=email,
                                         phone=phone,
                                         password=password))


@auth_api.route('/api/v1/login', methods=['POST'])
@jsonbody(email=features(type=str, required=True),
          password=features(type=str, required=True))
def login(email: str,
          password: str,
          login_user=LoginUser()):
    return SuccessResponse(login_user(email=email,
                                      password=password,
                                      login_method='email'))


@auth_api.route('/api/v1/token', methods=['POST'])
@jsonbody(refresh_token=features(type=str, required=True))
def get_token(refresh_token: str,
              get_access_token=GetAccessToken()):
    return SuccessResponse(get_access_token(refresh_token=refresh_token))


@auth_api.route('/api/v1/confirm', methods=['GET'])
@query_params(email=features(type=str, required=True),
              confirmation_code=features(type=str, required=True))
def confirm_registration(email: str,
                         confirmation_code: str,
                         confirm_user=ConfirmUser()):
    return confirm_user(email=email, confirmation_code=confirmation_code), 200


@auth_api.route('/api/v1/confirmation_code', methods=['GET'])
@query_params(email=features(type=str, required=True))
def send_confirmation_code(email: str,
                           send_email=SendEmail()):
    return SuccessResponse(send_email(email=email))
