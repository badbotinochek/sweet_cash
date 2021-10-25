
import pytest
import requests

HOST = 'http://127.0.0.1:5000'
EMAIL = "test@test.com"
PASSWORD = "test"


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


def test_login_wrong_password():
    response = requests.post(
        HOST + "/api/v1/login",
        json={
            "email": EMAIL,
            "password": "wrong"
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 403
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error": "Authentication Error",
        "message": "Wrong password"
    }


def test_login_invalid_email_format():
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


def test_login_wrong_email_type():
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


def test_login_wrong_password_type():
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

# @pytest.mark.freeze_time("2020-05-16")
# # @pytest.mark.usefixtures("dbsession", "mock_auth")
# def test_login_success():
#     response = requests.post(
#         HOST + "/api/v1/login",
#         json={
#               "email": "ag881.pst@gmail.com",
#               "password": "rksm911911Hh"
#              },
#         headers={"Content-Type": "application/json"},
#     )
#     assert response.status_code == 200
#     # assert response.json == {"result": True}


#
#
# if __name__ == '__main__':
#     try:
#         test_login_success()
#     except Exception as e:
#         print(e)
