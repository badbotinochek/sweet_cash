
import pytest
import requests

HOST = 'http://127.0.0.1:5000'
EMAIL = "test1@test.com"
PASSWORD = "1@yAndexru"

TOKEN = requests.post(
    HOST + "/api/v1/login",
    json={
        "email": EMAIL,
        "password": PASSWORD
    },
    headers={"Content-Type": "application/json"}
).json()["access_token"]

TRANSACTION_TYPE_ID = ''


'''
TEST CREATING TRANSACTION TYPE
'''


def test_create_transaction_type_success():
    global TRANSACTION_TYPE_ID
    response = requests.post(
        HOST + "/api/v1/transaction_type",
        json={
            "name": "1",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "id" in response.json()
    assert "name" in response.json()
    assert "description" in response.json()
    TRANSACTION_TYPE_ID = str(response.json()["id"])


def test_create_transaction_type_without_valid_token():
    response = requests.post(
        HOST + "/api/v1/transaction_type",
        json={
            "name": "1",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_create_transaction_type_without_body():
    response = requests.post(
        HOST + "/api/v1/transaction_type",
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_create_transaction_type_without_name():
    response = requests.post(
        HOST + "/api/v1/transaction_type",
        json={
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "name is required",
        "status": 400
    }


def test_create_transaction_type_without_description():
    response = requests.post(
        HOST + "/api/v1/transaction_type",
        json={
            "name": "1"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "id" in response.json()
    assert "name" in response.json()


def test_create_transaction_type_wrong_type_name():
    response = requests.post(
        HOST + "/api/v1/transaction_type",
        json={
            "name": 1,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for name",
        "status": 400
    }


def test_create_transaction_type_wrong_type_name_1():
    response = requests.post(
        HOST + "/api/v1/transaction_type",
        json={
            "name": -1,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for name",
        "status": 400
    }


def test_create_transaction_type_wrong_type_name_2():
    response = requests.post(
        HOST + "/api/v1/transaction_type",
        json={
            "name": 1.1,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for name",
        "status": 400
    }


def test_create_transaction_type_wrong_type_description():
    response = requests.post(
        HOST + "/api/v1/transaction_type",
        json={
            "name": "1",
            "description": 1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for description",
        "status": 400
    }


def test_create_transaction_type_wrong_type_description_1():
    response = requests.post(
        HOST + "/api/v1/transaction_type",
        json={
            "name": "1",
            "description": 1.2
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for description",
        "status": 400
    }


'''
TEST GETTING ALL TRANSACTION
'''


def test_get_transactions_type_success():
    response = requests.get(
        HOST + "/api/v1/transactions_types",
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(response.json()) is list
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]
    assert "description" in response.json()[0]
    assert "deleted" in response.json()[0]


def test_get_transactions_type_success_with_limit():
    response = requests.get(
        HOST + "/api/v1/transactions_types?limit=1",
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(response.json()) is list
    assert len(response.json()) == 1
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]
    assert "description" in response.json()[0]
    assert "deleted" in response.json()[0]


def test_get_transactions_type_success_with_offset():
    response = requests.get(
        HOST + "/api/v1/transactions_types?offset=0",
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(response.json()) is list
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]
    assert "description" in response.json()[0]
    assert "deleted" in response.json()[0]


def test_get_transactions_type_success_with_limit_and_offset():
    response = requests.get(
        HOST + "/api/v1/transactions_types?limit=1&offset=0",
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(response.json()) is list
    assert len(response.json()) == 1
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]
    assert "description" in response.json()[0]
    assert "deleted" in response.json()[0]


def test_get_transactions_type_without_valid_token():
    response = requests.get(
        HOST + "/api/v1/transactions_types",
        headers={"Authorization": ""}
    )
    assert response.status_code == 401


'''
TEST UPDATING TRANSACTION
'''


def test_update_transaction_type_success():
    response = requests.put(
        HOST + "/api/v1/transaction_type/" + TRANSACTION_TYPE_ID,
        json={
            "name": "1",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "id" in response.json()
    assert "name" in response.json()
    assert "description" in response.json()
    assert "deleted" in response.json()


def test_update_transaction_type_without_valid_token():
    response = requests.put(
        HOST + "/api/v1/transaction_type/" + TRANSACTION_TYPE_ID,
        json={
            "name": "1",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_update_transaction_type_without_body():
    response = requests.put(
        HOST + "/api/v1/transaction_type/" + TRANSACTION_TYPE_ID,
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_update_transaction_type_without_name():
    response = requests.put(
        HOST + "/api/v1/transaction_type/" + TRANSACTION_TYPE_ID,
        json={
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "name is required",
        "status": 400
    }


def test_update_transaction_type_without_description():
    response = requests.put(
        HOST + "/api/v1/transaction_type/" + TRANSACTION_TYPE_ID,
        json={
            "name": "1"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "id" in response.json()
    assert "name" in response.json()
    assert "description" in response.json()
    assert "deleted" in response.json()


def test_update_transaction_type_without_deleted():
    response = requests.put(
        HOST + "/api/v1/transaction_type/" + TRANSACTION_TYPE_ID,
        json={
            "name": "1"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "id" in response.json()
    assert "name" in response.json()
    assert "description" in response.json()
    assert "deleted" in response.json()


def test_update_transaction_type_wrong_type_name():
    response = requests.put(
        HOST + "/api/v1/transaction_type/" + TRANSACTION_TYPE_ID,
        json={
            "name": 1,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for name",
        "status": 400
    }


def test_update_transaction_type_wrong_type_name_1():
    response = requests.put(
        HOST + "/api/v1/transaction_type/" + TRANSACTION_TYPE_ID,
        json={
            "name": -1,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for name",
        "status": 400
    }


def test_update_transaction_type_wrong_type_name_2():
    response = requests.put(
        HOST + "/api/v1/transaction_type/" + TRANSACTION_TYPE_ID,
        json={
            "name": 1.1,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for name",
        "status": 400
    }


def test_update_transaction_type_wrong_type_description():
    response = requests.put(
        HOST + "/api/v1/transaction_type/" + TRANSACTION_TYPE_ID,
        json={
            "name": "1",
            "description": 1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for description",
        "status": 400
    }
