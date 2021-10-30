
from flask import jsonify, Blueprint
from datetime import datetime
import re
import logging

from db import db
from api.validator import jsonbody, features
from api.models.users import User
from api.models.session import Session
import api.errors as error

logger = logging.getLogger(name="auth")

auth_api = Blueprint('login', __name__)


@auth_api.route('/api/v1/login', methods=['POST'])
@jsonbody(email=features(type=str, required=True),
          password=features(type=str, required=True))
def login(email: str, password: str):
    if not check_email_format(email):
        raise error.APIParamError('Invalid email format')

    user = User.get_user(email)

    if user is None:
        user_id = create_new_user(name=email, email=email, password=password)
        token = new_token(user_id=user_id, login_method='email')
    else:
        if not user.check_password(password):
            logger.info(f'User {user.get_id()} with email {email} try to login with wrong password')
            raise error.APIAuthError('Wrong password')
        user_id = user.get_id()
        token = new_token(user_id=user_id, login_method='email')

    logger.info(f'User {user_id} login with email {email}')

    return jsonify({"access_token": token,
                    "user_id": user_id}), 200


def create_new_user(name: str, email: str, password: str):
    u = User(name=name, email=email, password=password)
    db.session.add(u)
    db.session.commit()
    logger.info(f'Create new user {u.get_id()} with email {email}')
    return u.get_id()


def check_email_format(email: str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    result = re.fullmatch(regex, email)
    return result


def new_token(user_id: str, login_method: str) -> str:
    session = Session.get(user_id=user_id)

    if session is not None:
        session.token = session.new_token()
        session.login_method = login_method
        session.updated = datetime.now().isoformat()
    else:
        session = Session(user_id=user_id, login_method=login_method)
        db.session.add(session)

    db.session.commit()

    return session.get_token()
