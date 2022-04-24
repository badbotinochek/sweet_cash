TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MDIyNjgzNCwianRpIjoiOTk0NTk5ZTMtMTk4Mi00NTk2LWEyNmEtNDkyOTlhNTg0YWRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjUwMjI2ODM0LCJleHAiOjE2NTIzMDA0MzR9.uP_oLwA0lOYws0'
HOST = 'http://127.0.0.1:5000'


'''
TEST CREATING TRANSACTION
'''


def test_create_transaction_for_manager_success(client, create_participant, create_transaction_category):
    tokens = create_participant[0]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "event_id": 1,
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert "id" in response
    assert "created_at" in response
    assert "event_id" in response
    assert "type" in response
    assert "category" in response
    assert "amount" in response
    assert "transaction_date" in response
    assert "receipt_id" in response
    assert "description" in response
    assert response['amount'] == 1.01
    assert response['category'] == "Тестовая категория 0"
    assert response['description'] == "description"
    assert response['event_id'] == 1
    assert response['id'] == 1
    assert response['number'] == 1
    assert response['receipt_id'] is None
    assert response['transaction_date'] == "Sun, 10 Oct 2021 04:25:03 GMT"
    assert response['type'] == "Income"
    assert response['updated_at'] is None
    assert response['user_id'] == 1


def test_create_transaction_for_partner_success(client, confirm_event, create_transaction_category):
    tokens = confirm_event[0]
    event_ids = confirm_event[2]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "event_id": event_ids[0],
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert "id" in response
    assert "created_at" in response
    assert "event_id" in response
    assert "type" in response
    assert "category" in response
    assert "amount" in response
    assert "transaction_date" in response
    assert "receipt_id" in response
    assert "description" in response
    assert response['amount'] == 1.01
    assert response['category'] == "Тестовая категория 0"
    assert response['description'] == "description"
    assert response['event_id'] == 1
    assert response['id'] == 1
    assert response['number'] == 1
    assert response['receipt_id'] is None
    assert response['transaction_date'] == "Sun, 10 Oct 2021 04:25:03 GMT"
    assert response['type'] == "Income"
    assert response['updated_at'] is None
    assert response['user_id'] == 3


def test_create_transaction_verified_observer_success(client, confirm_event, create_transaction_category):
    tokens = confirm_event[0]
    event_ids = confirm_event[2]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "event_id": event_ids[6],
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert "id" in response
    assert "created_at" in response
    assert "event_id" in response
    assert "type" in response
    assert "category" in response
    assert "amount" in response
    assert "transaction_date" in response
    assert "receipt_id" in response
    assert "description" in response
    assert response['amount'] == 1.01
    assert response['category'] == "Тестовая категория 0"
    assert response['description'] == "description"
    assert response['event_id'] == 7
    assert response['id'] == 1
    assert response['number'] == 1
    assert response['receipt_id'] is None
    assert response['transaction_date'] == "Sun, 10 Oct 2021 04:25:03 GMT"
    assert response['type'] == "Income"
    assert response['updated_at'] is None
    assert response['user_id'] == 4


def test_create_transaction_for_not_verified_partner(client, create_participant, create_transaction_category):
    tokens = create_participant[0]
    event_ids = create_participant[2]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "number": "12124f",
            "event_id": event_ids[0],
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Accepted user 3 not found in event 1"
    }


def test_create_transaction_for_not_verified_observer(client, create_participant, create_transaction_category):
    tokens = create_participant[0]
    event_ids = create_participant[2]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "number": "12124f",
            "event_id": event_ids[4],
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Accepted user 4 not found in event 5"
    }


def test_create_transaction_without_valid_token(client):
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "number": "12124f",
            "event_id": 1,
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "receipt_id": 1,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "msg": "Missing Authorization Header"
    }


def test_create_transaction_without_body(client, get_token):
    tokens = get_token[0]
    response = client.post(
        HOST + "/api/v1/transactions",
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_create_transaction_without_required_params(client, get_token):
    tokens = get_token[0]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={},
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('event_id', 'transaction_date', 'type', 'category', 'amount') required",
        "status": 400
    }


def test_create_transaction_with_wrong_types_for_params(client, get_token):
    tokens = get_token[0]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "number": 1,
            "event_id": "1313",
            "type": 1,
            "category": "1",
            "amount": -1,
            "transaction_date": 1231341,
            "receipt_id": "1",
            "description": 1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('event_id', 'transaction_date', 'type', "
                   "'category', 'amount', 'receipt_id', 'description')",
        "status": 400
    }


def test_create_transaction_with_invalid_event_id(client, create_events, create_transaction_category):
    tokens = create_events[0]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "number": "12124f",
            "event_id": -10,
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Participant for user 1 not found"
    }


def test_create_transaction_with_invalid_type(client, create_events, create_transaction_category):
    tokens = create_events[0]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "number": "12124f",
            "event_id": 1,
            "type": "Incoming",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "receipt_id": 1,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Request parameters error",
        "message": "Invalid transaction type Incoming"
    }


def test_create_transaction_with_invalid_category_id(client, create_events, create_transaction_category):
    tokens = create_events[0]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "number": "12124f",
            "event_id": 1,
            "type": "Income",
            "category": 0,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "receipt_id": 1,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Transaction category with id 0 not found"
    }


def test_create_transaction_with_invalid_amount_1(client, create_events, create_transaction_category):
    tokens = create_events[0]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "number": "12124f",
            "event_id": 1,
            "type": "Income",
            "category": 1,
            "amount": -1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "receipt_id": 1,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Request parameters error",
        "message": "Amount must be from 0 to 999999999999"
    }


def test_create_transaction_with_invalid_amount_2(client, create_events, create_transaction_category):
    tokens = create_events[0]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "number": "12124f",
            "event_id": 1,
            "type": "Income",
            "category": 1,
            "amount": 1000000000000000.0,
            "transaction_date": "2021-10-10T04:25:03Z",
            "receipt_id": 1,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Request parameters error",
        "message": "Amount must be from 0 to 999999999999"
    }


def test_create_transaction_with_invalid_receipt_id(client, create_events, create_transaction_category):
    tokens = create_events[0]
    response = client.post(
        HOST + "/api/v1/transactions",
        json={
            "number": "12124f",
            "event_id": 1,
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "receipt_id": 0,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Receipt with id 0 not found for user 1"
    }


'''
TEST GETTING TRANSACTION
'''


def test_get_one_transaction_for_manager_success(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.get(
        HOST + "/api/v1/transactions?ids=" + '1',
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 1
    response = response[0]
    assert "id" in response
    assert "created_at" in response
    assert "event_id" in response
    assert "type" in response
    assert "category" in response
    assert "amount" in response
    assert "transaction_date" in response
    assert "receipt_id" in response
    assert "description" in response
    assert len(response) == 12
    assert response['amount'] == 1.01
    assert response['category'] == "Тестовая категория 0"
    assert response['description'] == "description"
    assert response['event_id'] == 1
    assert response['id'] == 1
    assert response['number'] == 1
    assert response['receipt_id'] is None
    assert response['transaction_date'] == "Thu, 17 Feb 2022 04:25:03 GMT"
    assert response['type'] == "Income"
    assert response['updated_at'] is None
    assert response['user_id'] == 1


def test_get_two_transactions_for_manager_success(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.get(
        HOST + "/api/v1/transactions?ids=" '1,2',
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 2


def test_get_one_transaction_for_verified_observer_success(client, create_transactions_for_observer):
    tokens = create_transactions_for_observer[0]
    response = client.get(
        HOST + "/api/v1/transactions?ids=" + '1',
        headers={"Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 1
    response = response[0]
    assert "id" in response
    assert "created_at" in response
    assert "event_id" in response
    assert "type" in response
    assert "category" in response
    assert "amount" in response
    assert "transaction_date" in response
    assert "receipt_id" in response
    assert "description" in response
    assert len(response) == 12
    assert response['amount'] == 1.01
    assert response['category'] == "Тестовая категория 0"
    assert response['description'] == "description"
    assert response['event_id'] == 7
    assert response['id'] == 1
    assert response['number'] == 1
    assert response['receipt_id'] is None
    assert response['transaction_date'] == "Thu, 17 Feb 2022 04:25:03 GMT"
    assert response['type'] == "Income"
    assert response['updated_at'] is None
    assert response['user_id'] == 4


def test_get_one_transaction_for_verified_partner_success(client, create_transactions_for_partner):
    tokens = create_transactions_for_partner[0]
    response = client.get(
        HOST + "/api/v1/transactions?ids=" + '1',
        headers={"Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 1
    response = response[0]
    assert "id" in response
    assert "created_at" in response
    assert "event_id" in response
    assert "type" in response
    assert "category" in response
    assert "amount" in response
    assert "transaction_date" in response
    assert "receipt_id" in response
    assert "description" in response
    assert len(response) == 12
    assert response['amount'] == 1.01
    assert response['category'] == "Тестовая категория 0"
    assert response['description'] == "description"
    assert response['event_id'] == 1
    assert response['id'] == 1
    assert response['number'] == 1
    assert response['receipt_id'] is None
    assert response['transaction_date'] == "Thu, 17 Feb 2022 04:25:03 GMT"
    assert response['type'] == "Income"
    assert response['updated_at'] is None
    assert response['user_id'] == 3


def test_get_transaction_without_valid_token(client):
    response = client.get(
        HOST + "/api/v1/transactions?ids=" '1,2',
        headers={"Authorization": ""}
    )
    assert response.status_code == 401


def test_get_transaction_with_invalid_transaction_id(client, get_token):
    tokens = get_token[0]
    response = client.get(
        HOST + "/api/v1/transactions?ids=" '1,2',
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Transaction 1 not found for user 1"
    }


def test_get_one_transaction_for_not_verified_partner(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.get(
        HOST + "/api/v1/transactions?ids=" + '1',
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 1
    response = response[0]
    assert len(response) == 12
    assert response['amount'] == 1.01
    assert response['category'] == "Тестовая категория 0"
    assert response['description'] == "description"
    assert response['event_id'] == 1
    assert response['id'] == 1
    assert response['number'] == 1
    assert response['receipt_id'] is None
    assert response['transaction_date'] == "Thu, 17 Feb 2022 04:25:03 GMT"
    assert response['type'] == "Income"
    assert response['updated_at'] is None
    assert response['user_id'] == 1


def test_get_transaction_not_access(client, create_transactions_for_observer):
    tokens = create_transactions_for_observer[0]
    response = client.get(
        HOST + "/api/v1/transactions?ids=" + '1',
        headers={"Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Participant for user 3 not found"
    }


def test_get_deleted_transaction_for_manager_success(client, delete_transaction):
    tokens = delete_transaction[0]
    response = client.get(
        HOST + "/api/v1/transactions?ids=" + '1',
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 422
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "msg": "Not enough segments"
    }


'''
TEST GETTING ALL TRANSACTION
'''


def test_get_transactions_for_manager_success(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.get(
        HOST + "/api/v1/transactions/all?event_id=1&start=2022-02-15T16:29:10Z&end=2022-02-18T04:25:03Z",
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 5
    response = response[0]
    assert "id" in response
    assert "created_at" in response
    assert "event_id" in response
    assert "type" in response
    assert "category" in response
    assert "amount" in response
    assert "transaction_date" in response
    assert "receipt_id" in response
    assert "description" in response
    assert len(response) == 12
    assert response['amount'] == 1.01
    assert response['category'] == "Тестовая категория 0"
    assert response['description'] == "description"
    assert response['event_id'] == 1
    assert response['id'] == 5
    assert response['number'] == 5
    assert response['receipt_id'] is None
    assert response['transaction_date'] == "Thu, 17 Feb 2022 04:25:03 GMT"
    assert response['type'] == "Income"
    assert response['updated_at'] is None
    assert response['user_id'] == 1


def test_get_transactions_success_with_limit(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.get(
        HOST + "/api/v1/transactions/all?event_id=1&start=2022-02-15T16:29:10Z&end=2022-02-18T04:25:03Z&limit=1",
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 1


def test_get_transactions_success_with_offset(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.get(
        HOST + "/api/v1/transactions?offset=0",
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(response.get_json()) is list


def test_get_transactions_success_with_limit_and_offset(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.get(
        HOST + "/api/v1/transactions/all?event_id=1&start=2022-02-15T16:29:10Z&end=2022-02-18T04:25:03Z&limit=1&"
               "offset=0",
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(response.get_json()) is list
    assert len(response.get_json()) == 1


def test_get_transactions_without_valid_token(client):
    response = client.get(
        HOST + "/api/v1/transactions",
        headers={"Authorization": ""}
    )
    assert response.status_code == 401


def test_get_transactions_for_verified_observer_success(client, create_transactions_for_observer):
    tokens = create_transactions_for_observer[0]
    response = client.get(
        HOST + "/api/v1/transactions/all?event_id=7&start=2022-02-15T16:29:10Z&end=2022-02-18T04:25:03Z",
        headers={"Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 5
    response = response[0]
    assert "id" in response
    assert "created_at" in response
    assert "event_id" in response
    assert "type" in response
    assert "category" in response
    assert "amount" in response
    assert "transaction_date" in response
    assert "receipt_id" in response
    assert "description" in response
    assert len(response) == 12
    assert response['amount'] == 1.01
    assert response['category'] == "Тестовая категория 0"
    assert response['description'] == "description"
    assert response['event_id'] == 7
    assert response['id'] == 5
    assert response['number'] == 5
    assert response['receipt_id'] is None
    assert response['transaction_date'] == "Thu, 17 Feb 2022 04:25:03 GMT"
    assert response['type'] == "Income"
    assert response['updated_at'] is None
    assert response['user_id'] == 4


def test_get_transactions_for_verified_partner_success(client, create_transactions_for_partner):
    tokens = create_transactions_for_partner[0]
    response = client.get(
        HOST + "/api/v1/transactions/all?event_id=1&start=2022-02-15T16:29:10Z&end=2022-02-18T04:25:03Z",
        headers={"Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 5
    response = response[0]
    assert "id" in response
    assert "created_at" in response
    assert "event_id" in response
    assert "type" in response
    assert "category" in response
    assert "amount" in response
    assert "transaction_date" in response
    assert "receipt_id" in response
    assert "description" in response
    assert len(response) == 12
    assert response['amount'] == 1.01
    assert response['category'] == "Тестовая категория 0"
    assert response['description'] == "description"
    assert response['event_id'] == 1
    assert response['id'] == 5
    assert response['number'] == 5
    assert response['receipt_id'] is None
    assert response['transaction_date'] == "Thu, 17 Feb 2022 04:25:03 GMT"
    assert response['type'] == "Income"
    assert response['updated_at'] is None
    assert response['user_id'] == 3


def test_get_transactions_for_verified_observer_error(client, create_transactions_for_partner):
    tokens = create_transactions_for_partner[0]
    response = client.get(
        HOST + "/api/v1/transactions/all?event_id=7&start=2022-02-15T16:29:10Z&end=2022-02-18T04:25:03Z",
        headers={"Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Participant for user 3 not found"
    }


def test_get_transactions_for_verified_partner_error(client, create_transactions_for_observer):
    tokens = create_transactions_for_observer[0]
    response = client.get(
        HOST + "/api/v1/transactions/all?event_id=1&start=2022-02-15T16:29:10Z&end=2022-02-18T04:25:03Z",
        headers={"Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Participant for user 4 not found"
    }


'''
TEST UPDATING TRANSACTION
'''


def test_update_transaction_for_manager_success(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "id" in response.get_json()
    assert "created_at" in response.get_json()
    assert "type" in response.get_json()
    assert "category" in response.get_json()
    assert "amount" in response.get_json()
    assert "transaction_date" in response.get_json()
    assert "description" in response.get_json()


def test_update_transaction_without_valid_token(client):
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_update_transaction_without_body(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_update_transaction_with_invalid_transaction_id(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/0",
        json={
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Transaction 0 not found for user 1"
    }


def test_update_transaction_without_type(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('type',) required",
        "status": 400
    }


def test_update_transaction_without_category(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('category',) required",
        "status": 400
    }


def test_update_transaction_without_amount(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": 1,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('amount',) required",
        "status": 400
    }


def test_update_transaction_without_description(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "id" in response.get_json()
    assert "created_at" in response.get_json()
    assert "type" in response.get_json()
    assert "category" in response.get_json()
    assert "amount" in response.get_json()
    assert "transaction_date" in response.get_json()
    assert "description" in response.get_json()
    assert "description" == response.get_json()["description"]


def test_update_transaction_wrong_type_type(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": 1,
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('type',)",
        "status": 400
    }


def test_update_transaction_wrong_category_type(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": "1",
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('category',)",
        "status": 400
    }


def test_update_transaction_wrong_amount_type_1(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": 1,
            "amount": "1.01",
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('amount',)",
        "status": 400
    }


def test_update_transaction_wrong_amount_type_2(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": 1,
            "amount": 1,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('amount',)",
        "status": 400
    }


def test_update_transaction_wrong_transaction_date_type(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": 0,
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('transaction_date',)",
        "status": 400
    }


def test_update_transaction_wrong_description_type(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": 0
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('description',)",
        "status": 400
    }


def test_update_transaction_with_invalid_category_id(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": 0,
            "amount": 1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Transaction category with id 0 not found"
    }


def test_update_transaction_with_invalid_amount_1(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": 1,
            "amount": -1.01,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Request parameters error",
        "message": "Amount must be from 0 to 999999999999"
    }


def test_update_transaction_with_invalid_amount_2(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.put(
        HOST + "/api/v1/transactions/1",
        json={
            "type": "Income",
            "category": 1,
            "amount": 1000000000000000.0,
            "transaction_date": "2021-10-10T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Request parameters error",
        "message": "Amount must be from 0 to 999999999999"
    }


'''
TEST DELETING TRANSACTION
'''


def test_delete_transaction_for_manager_success(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.delete(
        HOST + "/api/v1/transactions/1",
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == '1 transactions deleted'


def test_delete_transaction_without_valid_token(client):
    response = client.delete(
        HOST + "/api/v1/transactions/1",
        headers={"Authorization": ""}
    )
    assert response.status_code == 401


def test_delete_transaction_with_invalid_transaction_id(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    response = client.delete(
        HOST + "/api/v1/transactions/0",
        headers={"Authorization": "Bearer " + TOKEN}
    )
    assert response.status_code == 422
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "msg": "Signature verification failed"
    }


def test_delete_transaction_for_partner_success(client, create_transactions_for_partner):
    tokens = create_transactions_for_partner[0]
    response = client.delete(
        HOST + "/api/v1/transactions/1",
        headers={"Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == '1 transactions deleted'


def test_delete_transaction_for_observer_success(client, create_transactions_for_observer):
    tokens = create_transactions_for_observer[0]
    response = client.delete(
        HOST + "/api/v1/transactions/1",
        headers={"Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == '1 transactions deleted'


def test_delete_transaction_for_partner_error(client, create_transactions_for_partner):
    tokens = create_transactions_for_partner[0]
    response = client.delete(
        HOST + "/api/v1/transactions/1",
        headers={"Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Participant for user 4 not found"
    }


def test_delete_transaction_for_observer_error(client, create_transactions_for_observer):
    tokens = create_transactions_for_observer[0]
    response = client.delete(
        HOST + "/api/v1/transactions/1",
        headers={"Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Participant for user 3 not found"
    }

