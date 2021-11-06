from flask import jsonify, Blueprint
import logging

from api.api import jsonbody, features
from api.services.auth import User

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
    return jsonify("Ok"), 200


@auth_api.route('/api/v1/login', methods=['POST'])
@jsonbody(email=features(type=str, required=True),
          password=features(type=str, required=True))
def login(email: str, password: str):
    return jsonify(User(email=email, password=password).login(login_method='email')), 200
