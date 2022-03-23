import requests

HOST = 'http://127.0.0.1:5000'
NAME = "testName"
EMAIL = "test1@test.com"
PHONE = '+79001234567'
PASSWORD = "1@yAndexru"
REFRESH_TOKEN = ''
TOKEN = ''

'''
TEST REGISTER
'''


def test_register_success(client):
    response = client.post(
        HOST + "/api/v1/auth/register",
        json={
            "name": NAME,
            "email": EMAIL,
            "phone": PHONE,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.get_json() == "Ok"
    assert response.headers["Content-Type"] == "application/json"


def test_register_without_body(client):
    response = client.post(
        HOST + "/api/v1/auth/register"
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_register_without_required_params(client):
    response = client.post(
        HOST + "/api/v1/auth/register",
        json={},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('name', 'email', 'phone', 'password') required",
        "status": 400
    }


def test_register_with_wrong_types_for_params(client):
    response = client.post(
        HOST + "/api/v1/auth/register",
        json={
            "name": 1,
            "email": 1,
            "phone": 1,
            "password": 1
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('name', 'email', 'phone', 'password')",
        "status": 400
    }


def test_register_with_invalid_email_format(client):
    response = client.post(
        HOST + "/api/v1/auth/register",
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
    assert response.get_json() == {
        "error": "Request parameters error",
        "message": "Invalid email format"
    }


def test_register_with_invalid_phone_format(client):
    response = client.post(
        HOST + "/api/v1/auth/register",
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
    assert response.get_json() == {
        "error": "Request parameters error",
        "message": "Invalid phone format"
    }


def test_register_with_invalid_password_format(client):
    response = client.post(
        HOST + "/api/v1/auth/register",
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
    assert response.get_json() == {
        "error": "Request parameters error",
        "message": "Invalid password format"
    }


def test_register_with_registered_email(client, added_new_user):
    response = client.post(
        HOST + "/api/v1/auth/register",
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
    assert response.get_json() == {
        "error": "Conflict",
        "message": "Email already registered"
    }


'''
TEST LOGIN
'''


def test_login_success(client, added_new_user):
    global REFRESH_TOKEN
    response = client.post(
        HOST + "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "refresh_token" in response.get_json()
    assert "user_id" in response.get_json()
    assert "auth_in_nalog_ru" in response.get_json()
    REFRESH_TOKEN = response.get_json()["refresh_token"]


def test_login_without_body(client):
    response = client.post(
        HOST + "/api/v1/auth/login"
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_login_without_required_params(client):
    response = client.post(
        HOST + "/api/v1/auth/login",
        json={},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('email', 'password') required",
        "status": 400
    }


def test_login_with_wrong_types_for_params(client):
    response = client.post(
        HOST + "/api/v1/auth/login",
        json={
            "email": 1,
            "password": 1
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('email', 'password')",
        "status": 400
    }


def test_login_with_new_refresh_token(client, added_new_user):
    global REFRESH_TOKEN
    response = client.post(
        HOST + "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "refresh_token" in response.get_json()
    assert "user_id" in response.get_json()
    assert "auth_in_nalog_ru" in response.get_json()
    assert response.get_json()["refresh_token"] != REFRESH_TOKEN
    REFRESH_TOKEN = response.get_json()["refresh_token"]


def test_login_with_wrong_password(client, added_new_user):
    response = client.post(
        HOST + "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": "1@yAndexru23"
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 403
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Authentication Error",
        "message": "Wrong password"
    }


def test_login_with_invalid_email_format(client, added_new_user):
    response = client.post(
        HOST + "/api/v1/auth/login",
        json={
            "email": "test",
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Request parameters error",
        "message": "Invalid email format"
    }


'''
TEST GETTING TOKEN
'''


def test_getting_token_success(client, added_new_user):
    global REFRESH_TOKEN, TOKEN
    response = client.post(
        HOST + "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    REFRESH_TOKEN = response.get_json()["refresh_token"]
    response = client.post(
        HOST + "/api/v1/auth/token",
        json={
            "refresh_token": REFRESH_TOKEN
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "refresh_token" in response.get_json()
    assert "token" in response.get_json()
    assert response.get_json()["refresh_token"] != REFRESH_TOKEN
    REFRESH_TOKEN = response.get_json()["refresh_token"]
    TOKEN = response.get_json()["token"]


def test_getting_token_without_body(client):
    response = client.post(
        HOST + "/api/v1/auth/token"
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_getting_token_without_required_params(client):
    response = client.post(
        HOST + "/api/v1/auth/token",
        json={},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('refresh_token',) required",
        "status": 400
    }


def test_getting_token_with_wrong_types_for_params(client):
    response = client.post(
        HOST + "/api/v1/auth/token",
        json={
            "refresh_token": 1
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('refresh_token',)",
        "status": 400
    }


def test_getting_new_token(client, added_new_user):
    global REFRESH_TOKEN, TOKEN
    response = client.post(
        HOST + "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    REFRESH_TOKEN = response.get_json()["refresh_token"]
    response = client.post(
        HOST + "/api/v1/auth/token",
        json={
            "refresh_token": REFRESH_TOKEN
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "refresh_token" in response.get_json()
    assert "token" in response.get_json()
    assert response.get_json()["refresh_token"] != REFRESH_TOKEN
    assert response.get_json()["token"] != TOKEN
    TOKEN = response.get_json()["token"]


def test_getting_token_with_old_refresh_token(client):
    response = client.post(
        HOST + "/api/v1/auth/token",
        json={
            "refresh_token": REFRESH_TOKEN
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Token not found"
    }


def test_getting_token_with_wrong_refresh_token(client):
    response = client.post(
        HOST + "/api/v1/auth/token",
        json={
            "refresh_token": "1"
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Token not found"
    }


'''
TEST CONFIRMATION USER
'''


def test_confirm_registration_success(client, added_new_user):
    response = client.get(
        HOST + "/api/v1/auth/confirm?email=" + EMAIL + "&code=1234"
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"


def test_confirm_registration_without_required_params(client):
    response = client.get(
        HOST + "/api/v1/auth/confirm"
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('email', 'code') required",
        "status": 400
    }


'''
TEST SENDING CONFIRM CODE
'''


def test_send_code_success(client):
    global REFRESH_TOKEN, TOKEN
    response = client.get(
        HOST + "/api/v1/auth/code?email=" + EMAIL
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


def test_send_code_without_required_params(client):
    response = client.get(
        HOST + "/api/v1/auth/code"
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('email',) required",
        "status": 400
    }
