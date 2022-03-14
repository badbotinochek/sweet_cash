from api.routes.auth import register
import pytest
import requests
from app import app

HOST = 'http://127.0.0.1:5000'
EMAIL = "test1@test.com"
PHONE = '+79001234567'
PASSWORD = "1@yAndexru"
REFRESH_TOKEN = ''
TOKEN = ''

def test_register_success():
    assert register(name = 1) == 200


def test_register_success1():
    response = requests.post(
        HOST + "/api/v1/auth/register",
        json={
            "name": EMAIL,
            "email": "test0@test.com",
            "phone": PHONE,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"