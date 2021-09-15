
from flask import request, jsonify, Blueprint

from db import db
from api.validator import jsonbody
from api.models.users import User


auth_api = Blueprint('login', __name__)


@auth_api.route('/api/v1/login', methods=['POST'])
@jsonbody(email=(str, "required"),
          password=(str, "required"))
def login():

    email = request.json.get('email')
    password = request.json.get('password')

    result = _login(name=email, email=email, password=password)

    return jsonify({"access_token": result["token"],
                    "user_id": result["user_id"]}), 200


def _login(name: str, email: str, password: str):

    def create_new_user(name: str, email: str, password: str):
        u = User(name=name, email=email, password=password)
        db.session.add(u)
        db.session.commit()
        return u.get_id(), u.get_token()

    try:
        user = User.authenticate(email=email, password=password)
        if user is not None:
            user_id = user.get_id()
            token = user.get_token()
        else:
            user_id, token = create_new_user(name=name, email=email, password=password)
    except Exception as e:
        print(e)
        user_id, token = create_new_user(name=name, email=email, password=password)

    return {
        "token": token,
        "user_id": user_id
        }
