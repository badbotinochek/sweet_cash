
import pytest
import requests

HOST = 'http://127.0.0.1:5000'
EMAIL = "test1@test.com"
PHONE = '+79001234567'
PASSWORD = "1@yAndexru"
TOKEN = None


'''
TEST REGISTER
'''


def test_register_success():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "phone": PHONE,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


def test_register_without_name():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "email": EMAIL,
            "phone": PHONE,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "name is required",
        "status": 400
    }


def test_register_without_email():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": EMAIL,
            "phone": PHONE,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "email is required",
        "status": 400
    }


def test_register_without_phone():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "phone is required",
        "status": 400
    }


def test_register_without_password():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "phone": PHONE
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "password is required",
        "status": 400
    }


def test_register_with_wrong_name_type():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": 1,
            "email": EMAIL,
            "phone": PHONE,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for name",
        "status": 400
    }


def test_register_with_wrong_email_type():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": EMAIL,
            "email": 1,
            "phone": PHONE,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for email",
        "status": 400
    }


def test_register_with_wrong_phone_type():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "phone": 1,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for phone",
        "status": 400
    }


def test_register_with_wrong_password_type():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "phone": PHONE,
            "password": 1
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for password",
        "status": 400
    }


def test_register_with_invalid_email_format():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": EMAIL,
            "email": '1212@121',
            "phone": PHONE,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error": "Request parameters Error",
        "message": "Invalid email format"
    }


def test_register_with_invalid_phone_format():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "phone": '12345',
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error": "Request parameters Error",
        "message": "Invalid phone format"
    }


def test_register_with_invalid_password_format():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "phone": PHONE,
            "password": '1231sssss'
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error": "Request parameters Error",
        "message": "Invalid password format"
    }


def test_register_without_body():
    response = requests.post(
        HOST + "/api/v1/register"
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_register_with_registered_email():
    response = requests.post(
        HOST + "/api/v1/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "phone": PHONE,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 409
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error": "Conflict",
        "message": "Email already registered"
    }


'''
TEST LOGIN
'''


def test_login_success():
    response = requests.post(
        HOST + "/api/v1/login",
        json={
            "email": EMAIL,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "access_token" in response.json()
    assert "user_id" in response.json()
    assert "auth_in_nalog_ru" in response.json()
    TOKEN = response.json()["access_token"]


def test_login_new_token():
    response = requests.post(
        HOST + "/api/v1/login",
        json={
            "email": EMAIL,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "access_token" in response.json()
    assert "user_id" in response.json()
    assert "auth_in_nalog_ru" in response.json()
    assert response.json()["access_token"] != TOKEN


def test_login_wrong_password():
    response = requests.post(
        HOST + "/api/v1/login",
        json={
            "email": EMAIL,
            "password": "1@yAndexru23"
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 403
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error": "Authentication Error",
        "message": "Wrong password"
    }


def test_login_without_email():
    response = requests.post(
        HOST + "/api/v1/login",
        json={
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "email is required",
        "status": 400
    }


def test_login_without_password():
    response = requests.post(
        HOST + "/api/v1/login",
        json={
            "email": EMAIL
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "password is required",
        "status": 400
    }


def test_login_with_wrong_email_type():
    response = requests.post(
        HOST + "/api/v1/login",
        json={
            "email": 1,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for email",
        "status": 400
    }


def test_login_with_wrong_password_type():
    response = requests.post(
        HOST + "/api/v1/login",
        json={
            "email": EMAIL,
            "password": 1
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for password",
        "status": 400
    }


def test_login_with_invalid_email_format():
    response = requests.post(
        HOST + "/api/v1/login",
        json={
            "email": "test",
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error": "Request parameters Error",
        "message": "Invalid email format"
    }


def test_login_without_body():
    response = requests.post(
        HOST + "/api/v1/login"
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }
