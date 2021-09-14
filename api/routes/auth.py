
from flask import request, jsonify, Blueprint
from api.validator import jsonbody
from api.models.users import User

auth_api = Blueprint('login', __name__)


@auth_api.route('/api/v1/login', methods=['POST'])
@jsonbody(email=(str, "required"),
          password=(str, "required"))
def login():

    email = request.json.get('email')
    password = request.json.get('password')

    # user = User.authenticate(email, password)
    #
    # token = user.get_token()
    token = ''
    return jsonify({'access_token': token}), 200
