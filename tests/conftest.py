import pytest
from pathlib import Path
from db import db

from app import create_app


HOST = 'http://127.0.0.1:5000'
NAME = "testName"
EMAIL = "test1@test.com"
PHONE = '+79001234567'
PASSWORD = "1@yAndexru"
REFRESH_TOKEN = ''
TOKEN = ''


@pytest.fixture()
def app():

    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    # other setup can go here

    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def added_new_user(client):
    client.post(
        HOST + "/api/v1/auth/register",
        json={
            "name": NAME,
            "email": EMAIL,
            "phone": PHONE,
            "password": PASSWORD
        },
    )






# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()


# get the resources folder in the tests folder
resources = Path(__file__).parent / "resources"


