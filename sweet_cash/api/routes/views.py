from flask import Blueprint
import logging

from sweet_cash.api.api import SuccessResponse, jsonbody, features, query_params
from sweet_cash.api.services.users.register_user import RegisterUser
from sweet_cash.api.services.users.login_user import LoginUser
from sweet_cash.api.services.users.get_access_token import GetAccessToken
from sweet_cash.api.services.users.confirm_user import ConfirmUser
from sweet_cash.api.services.email_sending.send_email import SendEmail

logger = logging.getLogger(name="views")

views_api = Blueprint('views', __name__)


@views_api.route('/', methods=['GET'])
def get_main_page():
    return open('sweet_cash/templates/main_page.html', 'r').read(), 200
