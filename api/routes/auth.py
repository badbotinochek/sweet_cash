
from flask import request, jsonify, Blueprint
from app import json_body_validator
from api.models.models import User

auth_api = Blueprint('login', __name__)


@auth_api.route('/api/v1/login', methods=['POST'])
@json_body_validator(email=(str, "required"),
                     password=(str, "required"))
def login():

    email = request.json.get('email')
    password = request.json.get('password')

    # user = User.authenticate(email, password)
    #
    # token = user.get_token()
    token = ''
    return jsonify({'access_token': token}), 200
