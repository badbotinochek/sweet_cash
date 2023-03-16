from flask import Blueprint
import logging

logger = logging.getLogger(name="views")

views_api = Blueprint('views', __name__)


@views_api.route('/', methods=['GET'])
def get_main_page():
    return open('sweet_cash/templates/main_page.html', 'r').read(), 200
