from flask import request, jsonify, Blueprint
import re

from db import db
from api.validator import jsonbody
from api.models.users import User
import api.errors as error

auth_api = Blueprint('login', __name__)


@auth_api.route('/api/v1/login', methods=['POST'])
@jsonbody(email=(str, "required"),
          password=(str, "required"))
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not check_email_format(email):
        raise error.APIParamError('Invalid email format')

    user = User.get_user(email)

    if user is None:
        user_id, token = create_new_user(name=email, email=email, password=password)
        return jsonify({"access_token": token,
                        "user_id": user_id}), 200
    else:
        if not user.check_password(password):
            raise error.APIAuthError('Wrong password')
        user_id = user.get_id()
        token = user.get_token()
        return jsonify({"access_token": token,
                        "user_id": user_id}), 200


def create_new_user(name: str, email: str, password: str):
    u = User(name=name, email=email, password=password)
    db.session.add(u)
    db.session.commit()
    return u.get_id(), u.get_token()


def check_email_format(email: str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    result = re.fullmatch(regex, email)
    return result
