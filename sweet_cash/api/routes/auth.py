from flask import Blueprint
import logging

from api.api import SuccessResponse, jsonbody, features
from api.services.register_user import RegisterUser
from api.services.login_user import LoginUser

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
