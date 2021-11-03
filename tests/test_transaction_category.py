
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

TRANSACTION_CATEGORY_ID = ''


'''
TEST CREATING TRANSACTION CATEGORY
'''


def test_create_transaction_category_success():
    global TRANSACTION_CATEGORY_ID
    response = requests.post(
        HOST + "/api/v1/transactions_category",
        json={
            "name": "1",
            "description": "description",
            "parent_category_id": 1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "id" in response.json()
    assert "name" in response.json()
    assert "parent_category_id" in response.json()
    assert "description" in response.json()
    TRANSACTION_CATEGORY_ID = str(response.json()["id"])


def test_create_transaction_category_without_valid_token():
    response = requests.post(
        HOST + "/api/v1/transactions_category",
        json={
            "name": "1",
            "description": "description",
            "parent_category_id": 1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_create_transaction_category_without_body():
    response = requests.post(
        HOST + "/api/v1/transactions_category",
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_create_transaction_category_without_name():
    response = requests.post(
        HOST + "/api/v1/transactions_category",
        json={
            "description": "description",
            "parent_category_id": 1
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


def test_create_transaction_category_without_description():
    response = requests.post(
        HOST + "/api/v1/transactions_category",
        json={
            "name": "1",
            "parent_category_id": 1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "id" in response.json()
    assert "name" in response.json()
    assert "parent_category_id" in response.json()
    assert "description" in response.json()


def test_create_transaction_category_without_parent_category():
    response = requests.post(
        HOST + "/api/v1/transactions_category",
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
    assert "parent_category_id" in response.json()
    assert "description" in response.json()


def test_create_transaction_category_with_invalid_parent_category_id():
    response = requests.post(
        HOST + "/api/v1/transactions_category",
        json={
            "name": "1",
            "description": "description",
            "parent_category_id": "1"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for parent_category_id",
        "status": 400
    }


def test_create_transaction_category_with_invalid_parent_category_id1():
    response = requests.post(
        HOST + "/api/v1/transactions_category",
        json={
            "name": "1",
            "description": "description",
            "parent_category_id": -1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error": "Not found",
        "message": "Parent category with id -1 not found"
    }


def test_create_transaction_category_wrong_type_name():
    response = requests.post(
        HOST + "/api/v1/transactions_category",
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


def test_create_transaction_category_wrong_type_description():
    response = requests.post(
        HOST + "/api/v1/transactions_category",
        json={
            "name": "1",
            "description": 1,
            "parent_category_id": 1
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


def test_create_transaction_category_wrong_type_parent_id():
    response = requests.post(
        HOST + "/api/v1/transactions_category",
        json={
            "name": "1",
            "description": 1.2,
            "parent_category_id": "1"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for parent_category_id",
        "status": 400
    }


'''
TEST GETTING ALL TRANSACTION CATEGORY
'''


def test_get_transactions_category_success():
    response = requests.get(
        HOST + "/api/v1/transactions/categories",
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(response.json()) is list
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]
    assert "description" in response.json()[0]
    assert "parent_category_id" in response.json()[0]


def test_get_transactions_category_success_with_limit():
    response = requests.get(
        HOST + "/api/v1/transactions/categories?limit=1",
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(response.json()) is list
    assert len(response.json()) == 1
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]
    assert "description" in response.json()[0]
    assert "parent_category_id" in response.json()[0]


def test_get_transactions_category_success_with_offset():
    response = requests.get(
        HOST + "/api/v1/transactions/categories?offset=0",
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(response.json()) is list
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]
    assert "description" in response.json()[0]
    assert "parent_category_id" in response.json()[0]


def test_get_transactions_category_success_with_limit_and_offset():
    response = requests.get(
        HOST + "/api/v1/transactions/categories?limit=1&offset=0",
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(response.json()) is list
    assert len(response.json()) == 1
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]
    assert "description" in response.json()[0]
    assert "parent_category_id" in response.json()[0]


def test_get_transactions_category_without_valid_token():
    response = requests.get(
        HOST + "/api/v1/transactions/categories",
        headers={"Authorization": ""}
    )
    assert response.status_code == 401


'''
TEST UPDATING TRANSACTION CATEGORY
'''


def test_update_transaction_category_success():
    response = requests.put(
        HOST + "/api/v1/transactions_category/" + TRANSACTION_CATEGORY_ID,
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
    assert "parent_category_id" in response.json()


def test_update_transaction_category_without_valid_token():
    response = requests.put(
        HOST + "/api/v1/transactions_category/" + TRANSACTION_CATEGORY_ID,
        json={
            "name": "1",
            "description": "description",
            "deleted": "2021-10-10T04:25:03Z",
            "parent_category_id": 345
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_update_transaction_category_without_body():
    response = requests.put(
        HOST + "/api/v1/transactions_category/" + TRANSACTION_CATEGORY_ID,
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_update_transaction_category_without_name():
    response = requests.put(
        HOST + "/api/v1/transactions_category/" + TRANSACTION_CATEGORY_ID,
        json={
            "description": "description",
            "deleted": "2021-10-10T04:25:03Z",
            "parent_category_id": 345
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


def test_update_transaction_category_without_description():
    response = requests.put(
        HOST + "/api/v1/transactions_category/" + TRANSACTION_CATEGORY_ID,
        json={
            "name": "90",
            "parent_category_id": 1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "id" in response.json()
    assert "name" in response.json()
    assert "description" in response.json()
    assert "parent_category_id" in response.json()


def test_update_transaction_category_without_parent_category_id():
    response = requests.put(
        HOST + "/api/v1/transactions_category/" + TRANSACTION_CATEGORY_ID,
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
    assert "parent_category_id" in response.json()


def test_update_transaction_category_wrong_type_name():
    response = requests.put(
        HOST + "/api/v1/transactions_category/" + TRANSACTION_CATEGORY_ID,
        json={
            "name": 1,
            "description": "description",
            "parent_category_id": 345
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


def test_update_transaction_category_wrong_type_description():
    response = requests.put(
        HOST + "/api/v1/transactions_category/" + TRANSACTION_CATEGORY_ID,
        json={
            "name": "1",
            "description": 1,
            "parent_category_id": 345
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


def test_update_transaction_category_wrong_type_parent_category_id():
    response = requests.put(
        HOST + "/api/v1/transactions_category/" + TRANSACTION_CATEGORY_ID,
        json={
            "name": "1",
            "description": "1",
            "parent_category_id": "345"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for parent_category_id",
        "status": 400
    }


def test_update_transaction_category_with_invalid_parent_category_id1():
    response = requests.put(
        HOST + "/api/v1/transactions_category/1",
        json={
            "name": "1",
            "description": "description",
            "parent_category_id": -1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error": "Not found",
        "message": "Parent category with id -1 not found"
    }


def test_update_transaction_category_with_invalid_transaction_category_id():
    response = requests.put(
        HOST + "/api/v1/transactions_category/40000",
        json={
            "name": "1",
            "description": "1"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error": "Not found",
        "message": "Transaction category 40000 not found"
    }
