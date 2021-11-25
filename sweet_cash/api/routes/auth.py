from flask import Blueprint
import logging

from api.api import SuccessResponse, jsonbody, features
from api.dependencies import register_user_, login_user_

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
             password: str):
    return SuccessResponse(register_user_(name=name,
                                          email=email,
                                          phone=phone,
                                          password=password)())


@auth_api.route('/api/v1/login', methods=['POST'])
@jsonbody(email=features(type=str, required=True),
          password=features(type=str, required=True))
def login(email: str, password: str):
    return SuccessResponse(login_user_(email=email,
                                       password=password,
                                       login_method='email')())
