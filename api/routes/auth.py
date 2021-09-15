
from flask import request, jsonify, Blueprint
from api.validator import jsonbody
from api.models.users import db, User

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
    try:
        user = User.authenticate(email=email, password=password)
        token = user.get_token()
    except Exception as e:
        print(e)
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        token = user.get_token()

    return {
        "token": token,
        "user_id": user.get_id()
        }
