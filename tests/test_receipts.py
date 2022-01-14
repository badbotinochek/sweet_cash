
import pytest
import requests

HOST = 'http://127.0.0.1:5000'
EMAIL = "test1@test.com"
PASSWORD = "1@yAndexru"

REFRESH_TOKEN = requests.post(
    HOST + "/api/v1/login",
    json={
        "email": EMAIL,
        "password": PASSWORD
    },
    headers={"Content-Type": "application/json"}
).json()["refresh_token"]

TOKEN = requests.post(
    HOST + "/api/v1/token",
    json={
        "refresh_token": REFRESH_TOKEN
    },
    headers={"Content-Type": "application/json"}
).json()["token"]

TRANSACTION_ID = ''


'''
TEST SENDING SMS WITH OTP
'''


def test_send_sms_without_token():
    global TRANSACTION_ID
    response = requests.post(
        HOST + "/api/v1/nalog/otp/send",
        headers={
            "Content-Type": "0",
            "Authorization": ""
        }
    )
    assert response.status_code == 401


# def test_create_transaction_success():
#     global TRANSACTION_ID
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
#     assert "id" in response.json()
#     assert "created_at" in response.json()
#     assert "type" in response.json()
#     assert "category" in response.json()
#     assert "amount" in response.json()
#     assert "transaction_date" in response.json()
#     assert "private" in response.json()
#     assert "description" in response.json()
#     TRANSACTION_ID = str(response.json()["id"])
#
#
# def test_create_transaction_without_valid_token():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": ""}
#     )
#     assert response.status_code == 401
#
#
# def test_create_transaction_without_body():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         headers={"Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Json required",
#         "status": 400
#     }
#
#
# def test_create_transaction_without_type():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "type is required",
#         "status": 400
#     }
#
#
# def test_create_transaction_without_category():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "category is required",
#         "status": 400
#     }
#
#
# def test_create_transaction_without_amount():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "amount is required",
#         "status": 400
#     }
#
#
# def test_create_transaction_without_transaction_date():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "transaction_date is required",
#         "status": 400
#     }
#
#
# def test_create_transaction_without_private():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "private is required",
#         "status": 400
#     }
#
#
# def test_create_transaction_without_description():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
#     assert "id" in response.json()
#     assert "created_at" in response.json()
#     assert "type" in response.json()
#     assert "category" in response.json()
#     assert "amount" in response.json()
#     assert "transaction_date" in response.json()
#     assert "private" in response.json()
#     assert "description" in response.json()
#     assert response.json()["description"] is None
#
#
# def test_create_transaction_wrong_type_type():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": 1,
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for type",
#         "status": 400
#     }
#
#
# def test_create_transaction_wrong_category_type():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": "1",
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for category",
#         "status": 400
#     }
#
#
# def test_create_transaction_wrong_amount_type_1():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": "1.01",
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for amount",
#         "status": 400
#     }
#
#
# def test_create_transaction_wrong_amount_type_2():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for amount",
#         "status": 400
#     }
#
#
# def test_create_transaction_wrong_transaction_date_type():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": 0,
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for transaction_date",
#         "status": 400
#     }
#
#
# def test_create_transaction_wrong_private_type():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": 1,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for private",
#         "status": 400
#     }
#
#
# def test_create_transaction_wrong_description_type():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": 0
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for description",
#         "status": 400
#     }
#
#
# def test_create_transaction_with_invalid_type_id():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Incoming",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 404
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error": "Not found",
#         "message": "Invalid transaction type Incoming"
#     }
#
#
# def test_create_transaction_with_invalid_category_id():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 0,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 404
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error": "Not found",
#         "message": "Transaction category with id 0 not found"
#     }
#
#
# def test_create_transaction_with_invalid_amount_1():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": -1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error": "Request parameters Error",
#         "message": "Amount must be from 0 to 999999999999"
#     }
#
#
# def test_create_transaction_with_invalid_amount_2():
#     response = requests.post(
#         HOST + "/api/v1/transaction",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1000000000000000.0,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error": "Request parameters Error",
#         "message": "Amount must be from 0 to 999999999999"
#     }
#
#
# '''
# TEST GETTING ONE TRANSACTION
# '''
#
#
# def test_get_transaction_success():
#     response = requests.get(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         headers={"Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
#     assert "id" in response.json()
#     assert "created_at" in response.json()
#     assert "type" in response.json()
#     assert "category" in response.json()
#     assert "amount" in response.json()
#     assert "transaction_date" in response.json()
#     assert "private" in response.json()
#     assert "description" in response.json()
#
#
# def test_get_transaction_without_valid_token():
#     response = requests.get(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         headers={"Authorization": ""}
#     )
#     assert response.status_code == 401
#
#
# def test_get_transaction_with_invalid_transaction_id():
#     response = requests.get(
#         HOST + "/api/v1/transaction/0",
#         headers={"Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 404
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error": "Not found",
#         "message": "Transaction 0 not found"
#     }
#
#
# '''
# TEST GETTING ALL TRANSACTION
# '''
#
#
# def test_get_transactions_success():
#     response = requests.get(
#         HOST + "/api/v1/transactions",
#         headers={"Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
#     assert type(response.json()) is list
#     assert "id" in response.json()[0]
#     assert "created_at" in response.json()[0]
#     assert "type" in response.json()[0]
#     assert "category" in response.json()[0]
#     assert "amount" in response.json()[0]
#     assert "transaction_date" in response.json()[0]
#     assert "private" in response.json()[0]
#     assert "description" in response.json()[0]
#
#
# def test_get_transactions_success_with_limit():
#     response = requests.get(
#         HOST + "/api/v1/transactions?limit=1",
#         headers={"Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
#     assert type(response.json()) is list
#     assert len(response.json()) == 1
#     assert "id" in response.json()[0]
#     assert "created_at" in response.json()[0]
#     assert "type" in response.json()[0]
#     assert "category" in response.json()[0]
#     assert "amount" in response.json()[0]
#     assert "transaction_date" in response.json()[0]
#     assert "private" in response.json()[0]
#     assert "description" in response.json()[0]
#
#
# def test_get_transactions_success_with_offset():
#     response = requests.get(
#         HOST + "/api/v1/transactions?offset=0",
#         headers={"Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
#     assert type(response.json()) is list
#     assert "id" in response.json()[0]
#     assert "created_at" in response.json()[0]
#     assert "type" in response.json()[0]
#     assert "category" in response.json()[0]
#     assert "amount" in response.json()[0]
#     assert "transaction_date" in response.json()[0]
#     assert "private" in response.json()[0]
#     assert "description" in response.json()[0]
#
#
# def test_get_transactions_success_with_limit_and_offset():
#     response = requests.get(
#         HOST + "/api/v1/transactions?limit=1&offset=0",
#         headers={"Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
#     assert type(response.json()) is list
#     assert len(response.json()) == 1
#     assert "id" in response.json()[0]
#     assert "created_at" in response.json()[0]
#     assert "type" in response.json()[0]
#     assert "category" in response.json()[0]
#     assert "amount" in response.json()[0]
#     assert "transaction_date" in response.json()[0]
#     assert "private" in response.json()[0]
#     assert "description" in response.json()[0]
#
#
# def test_get_transactions_without_valid_token():
#     response = requests.get(
#         HOST + "/api/v1/transactions",
#         headers={"Authorization": ""}
#     )
#     assert response.status_code == 401
#
#
# '''
# TEST UPDATING TRANSACTION
# '''
#
#
# def test_update_transaction_success():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
#     assert "id" in response.json()
#     assert "created_at" in response.json()
#     assert "type" in response.json()
#     assert "category" in response.json()
#     assert "amount" in response.json()
#     assert "transaction_date" in response.json()
#     assert "private" in response.json()
#     assert "description" in response.json()
#
#
# def test_update_transaction_without_valid_token():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": ""}
#     )
#     assert response.status_code == 401
#
#
# def test_update_transaction_without_body():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         headers={"Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Json required",
#         "status": 400
#     }
#
#
# def test_update_transaction_with_invalid_transaction_id():
#     response = requests.put(
#         HOST + "/api/v1/transaction/0",
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 404
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error": "Not found",
#         "message": "Transaction 0 not found"
#     }
#
#
# def test_update_transaction_without_type():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "type is required",
#         "status": 400
#     }
#
#
# def test_update_transaction_without_category():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "category is required",
#         "status": 400
#     }
#
#
# def test_update_transaction_without_amount():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "amount is required",
#         "status": 400
#     }
#
#
# def test_update_transaction_without_transaction_date():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "transaction_date is required",
#         "status": 400
#     }
#
#
# def test_update_transaction_without_private():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "private is required",
#         "status": 400
#     }
#
#
# def test_update_transaction_without_description():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
#     assert "id" in response.json()
#     assert "created_at" in response.json()
#     assert "type" in response.json()
#     assert "category" in response.json()
#     assert "amount" in response.json()
#     assert "transaction_date" in response.json()
#     assert "private" in response.json()
#     assert "description" in response.json()
#     assert "description" == response.json()["description"]
#
#
# def test_update_transaction_wrong_type_type():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": 1,
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for type",
#         "status": 400
#     }
#
#
# def test_update_transaction_wrong_category_type():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": "1",
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for category",
#         "status": 400
#     }
#
#
# def test_update_transaction_wrong_amount_type_1():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": "1.01",
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for amount",
#         "status": 400
#     }
#
#
# def test_update_transaction_wrong_amount_type_2():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for amount",
#         "status": 400
#     }
#
#
# def test_update_transaction_wrong_transaction_date_type():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": 0,
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for transaction_date",
#         "status": 400
#     }
#
#
# def test_update_transaction_wrong_private_type():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": 1,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for private",
#         "status": 400
#     }
#
#
# def test_update_transaction_wrong_description_type():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": 0
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error_code": "bad-params",
#         "message": "Invalid type for description",
#         "status": 400
#     }
#
#
# def test_update_transaction_with_invalid_type_id():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Incoming",
#             "category": 1,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 404
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error": "Not found",
#         "message": "Invalid transaction type Incoming"
#     }
#
#
# def test_update_transaction_with_invalid_category_id():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 0,
#             "amount": 1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 404
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error": "Not found",
#         "message": "Transaction category with id 0 not found"
#     }
#
#
# def test_update_transaction_with_invalid_amount_1():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": -1.01,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error": "Request parameters Error",
#         "message": "Amount must be from 0 to 999999999999"
#     }
#
#
# def test_update_transaction_with_invalid_amount_2():
#     response = requests.put(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         json={
#             "type": "Income",
#             "category": 1,
#             "amount": 1000000000000000.0,
#             "transaction_date": "2021-10-10T04:25:03Z",
#             "private": False,
#             "description": "description"
#         },
#         headers={"Content-Type": "application/json",
#                  "Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 400
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error": "Request parameters Error",
#         "message": "Amount must be from 0 to 999999999999"
#     }
#
#
# '''
# TEST DELETING TRANSACTION
# '''
#
#
# def test_delete_transaction_success():
#     response = requests.delete(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         headers={"Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == 'Ok'
#
#
# def test_delete_transaction_without_valid_token():
#     response = requests.delete(
#         HOST + "/api/v1/transaction/" + TRANSACTION_ID,
#         headers={"Authorization": ""}
#     )
#     assert response.status_code == 401
#
#
# def test_delete_transaction_with_invalid_transaction_id():
#     response = requests.delete(
#         HOST + "/api/v1/transaction/0",
#         headers={"Authorization": "Bearer " + TOKEN}
#     )
#     assert response.status_code == 404
#     assert response.headers["Content-Type"] == "application/json"
#     assert response.json() == {
#         "error": "Not found",
#         "message": "Transaction 0 not found"
#     }
