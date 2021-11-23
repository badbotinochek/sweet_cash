from flask import Blueprint
import logging

from api.api import Response, jsonbody, features
from api.services.user import User

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
    User(name=name,
         email=email,
         phone=phone,
         password=password).register()
    return Response.success()


@auth_api.route('/api/v1/login', methods=['POST'])
@jsonbody(email=features(type=str, required=True),
          password=features(type=str, required=True))
def login(email: str, password: str):
    result = User(email=email,
                  password=password,
                  login_method='email').login()
    return Response.success(result)
