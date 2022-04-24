import pytest
from pathlib import Path
from db import db
import psycopg2
from datetime import datetime
import time
import bcrypt
from api.models.users import UserModel

from app import create_app
# from api.services.users.register_user import RegisterUser
# from tests.test_api.test_services.test_users.test_register_user import test_register

HOST = 'http://127.0.0.1:5000'
NAME = "testName"
EMAIL = "test1@test.com"
PHONE = '+79001234567'
PASSWORD = "1@yAndexru"
REFRESH_TOKEN = ''
TOKEN = ''


@pytest.fixture(autouse=True)
def footer_function_scope():
    """Отображает продолжительность теста после каждой функции."""
    start = time.time()
    yield
    stop = time.time()
    delta = stop - start
    print('\ntest duration : {:0.3} seconds'.format(delta))


def delete_date():
    """Удаление всех данных во всех таблицах"""
    conn = psycopg2.connect(
        database="test",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432"
    )

    # Open a cursor to perform database operations
    cursor = conn.cursor()

    list_table_DB = ('events', 'events_participants', 'nalog_ru_sessions', 'receipts', 'sessions', 'transactions',
                     'transactions_categories', 'users')

    # Execute a query
    for i in list_table_DB:
        cursor.execute(f"TRUNCATE table {i}")

    conn.commit()
    cursor.close()
    conn.close()


@pytest.fixture()
def deleted_date():
    yield
    """Удаление всех данных во всех таблицах"""
    conn = psycopg2.connect(
        database="test",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432"
    )

    # Open a cursor to perform database operations
    cursor = conn.cursor()

    list_table_DB = ('events', 'events_participants', 'nalog_ru_sessions', 'receipts', 'sessions', 'transactions',
                     'transactions_categories', 'users')

    # Execute a query
    for i in list_table_DB:
        cursor.execute(f"TRUNCATE table {i}")

    conn.commit()
    cursor.close()
    conn.close()


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    # other setup can go here

    yield app
        # DROP SCHEMA public
    # # clean up / reset resources here


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


# @pytest.fixture()
# def added_new_users(client):
#     """Регистрация в системе 4-х пользователей"""
#     user_email = (lambda n: f'test{n}@test.com')
#     password = "1@yAndexru"
#     for i in range(1, 5):
#         client.post(
#             HOST + "/api/v1/auth/register",
#             json={
#                 "name": NAME,
#                 "email": user_email(i),
#                 "phone": PHONE,
#                 "password": password
#             },
#         )
#     yield
#     delete_date()


@pytest.fixture()
def added_new_users():
    """Регистрация в системе 4-х пользователей"""
    conn = psycopg2.connect(
        database="test",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432"
    )

    # Open a cursor to perform database operations
    cursor = conn.cursor()

    for i in range(1, 5):
        cursor.execute("INSERT INTO users (created_at, name, email, phone, password, confirmed) "
                       "VALUES (%s, %s, %s, %s, %s, %s)", (
                            datetime.utcnow(),
                            f"test{i}@test.com",
                            f"test{i}@test.com",
                            "+79001234567",
                            bcrypt.hashpw("1@yAndexru".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                            True))
    conn.commit()
    cursor.close()
    conn.close()
    yield
    delete_date()


@pytest.fixture()
def get_token(client, added_new_users):
    user_email = (lambda n: f'test{n}@test.com')
    password = "1@yAndexru"
    user_ids = []
    tokens = []

    for i in range(1, 5):
        login_response = client.post(
            HOST + "/api/v1/auth/login",
            json={
                "email": user_email(i),
                "password": password
            },
            headers={"Content-Type": "application/json"}
        )

        refresh_token = login_response.get_json()["refresh_token"]
        user_ids.append(login_response.get_json()["user_id"])

        token = client.post(
            HOST + "/api/v1/auth/token",
            json={
                "refresh_token": refresh_token
            },
            headers={"Content-Type": "application/json"}
        ).get_json()["token"]
        tokens.append(token)
    return tokens, user_ids


@pytest.fixture()
def create_events(client, get_token):
    tokens = get_token[0]
    user_ids = get_token[1]
    event_ids = []
    for i in range(0, 10):
        if i < 5:
            response = client.post(
                HOST + "/api/v1/events",
                json={
                    "name": "Событие",
                    "start": "2022-02-01T04:25:03Z",
                    "end": "2022-03-01T04:25:03Z",
                    "description": "description"
                },
                headers={"Content-Type": "application/json",
                         "Authorization": "Bearer " + tokens[0]}
            )
            event_ids.append(response.get_json()["id"])
        else:
            response = client.post(
                HOST + "/api/v1/events",
                json={
                    "name": "Событие",
                    "start": "2022-02-01T04:25:03Z",
                    "end": "2022-03-01T04:25:03Z",
                    "description": "description"
                },
                headers={"Content-Type": "application/json",
                         "Authorization": "Bearer " + tokens[1]}
            )
            event_ids.append(response.get_json()["id"])

    return tokens, user_ids, event_ids


@pytest.fixture()
def create_participant(client, create_events):
    tokens = create_events[0]
    user_ids = create_events[1]
    event_ids = create_events[2]
    role = ["Partner", "Observer"]
    participant_ids = []
    for i in range(0, 5):
        response = client.post(
            HOST + "/api/v1/events/" + str(event_ids[i]) + "/participant",
            json={
                "user_id": user_ids[2],
                "role": role[0]
            },
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + tokens[0]}
        )
        participant_ids.append(response.get_json()["id"])
        if i == 4:
            response = client.post(
                HOST + "/api/v1/events/" + str(event_ids[i]) + "/participant",
                json={
                    "user_id": user_ids[3],
                    "role": role[0]
                },
                headers={"Content-Type": "application/json",
                         "Authorization": "Bearer " + tokens[0]}
            )
            participant_ids.append(response.get_json()["id"])
    for i in range(6, 10):
        response = client.post(
            HOST + "/api/v1/events/" + str(event_ids[i]) + "/participant",
            json={
                "user_id": user_ids[3],
                "role": role[1]
            },
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + tokens[1]}
        )
        participant_ids.append(response.get_json()["id"])
    return tokens, user_ids, event_ids, participant_ids


@pytest.fixture()
def confirm_event(client, create_participant):
    tokens = create_participant[0]
    user_ids = create_participant[1]
    event_ids = create_participant[2]
    participant_ids = create_participant[2]
    client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/confirm",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
        )
    client.put(
        HOST + "/api/v1/events/" + str(event_ids[6]) + "/participant/confirm",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[3]}
        )
    return tokens, user_ids, event_ids, participant_ids


@pytest.fixture()
def create_transaction_category():
    conn = psycopg2.connect(
        database="test",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432"
    )

    # Open a cursor to perform database operations
    cursor = conn.cursor()

    # Execute a query
    for i in range(6):
        cursor.execute("INSERT INTO transactions_categories (created_at, name, parent_category_id) "
                       "VALUES (%s, %s, %s)",
                       (datetime.utcnow(), f"Тестовая категория {i}", i))

    conn.commit()
    cursor.close()
    conn.close()


@pytest.fixture()
def create_transactions_for_manager(client, create_events, create_transaction_category):
    tokens = create_events[0]
    user_ids = create_events[1]
    event_ids = create_events[2]
    for i in range(5):
        for m in range(5):
            client.post(
                HOST + "/api/v1/transactions",
                json={
                    "number": "12124f",
                    "event_id": i,
                    "type": "Income",
                    "category": 1,
                    "amount": 1.01,
                    "transaction_date": "2022-02-17T04:25:03Z",
                    "description": "description"
                },
                headers={"Content-Type": "application/json",
                         "Authorization": "Bearer " + tokens[0]}
            )
    client.post(
        HOST + "/api/v1/transactions",
        json={
            "number": "12124f",
            "event_id": 1,
            "type": "Income",
            "category": 1,
            "amount": 1.01,
            "transaction_date": "2022-03-17T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
            )
    return tokens, user_ids, event_ids


@pytest.fixture()
def create_transactions_for_partner(client, confirm_event, create_transaction_category):
    tokens = confirm_event[0]
    user_ids = confirm_event[1]
    event_ids = confirm_event[2]
    for i in range(5):
        client.post(
            HOST + "/api/v1/transactions",
            json={
                "event_id": 1,
                "type": "Income",
                "category": 1,
                "amount": 1.01,
                "transaction_date": "2022-02-17T04:25:03Z",
                "description": "description"
                },
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + tokens[2]}
            )
    return tokens, user_ids, event_ids


@pytest.fixture()
def create_transactions_for_observer(client, confirm_event, create_transaction_category):
    tokens = confirm_event[0]
    user_ids = confirm_event[1]
    event_ids = confirm_event[2]
    for i in range(5):
        client.post(
            HOST + "/api/v1/transactions",
            json={
                "event_id": 7,
                "type": "Income",
                "category": 1,
                "amount": 1.01,
                "transaction_date": "2022-02-17T04:25:03Z",
                "description": "description"
                },
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + tokens[3]}
            )
    return tokens, user_ids, event_ids


@pytest.fixture()
def delete_transaction(client, create_transactions_for_manager):
    tokens = create_transactions_for_manager[0]
    client.delete(
        HOST + "/api/v1/transactions/1",
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    return tokens


# @pytest.fixture()
# def delete_transaction_status(client, create_transactions_for_manager):
#     tokens = create_transactions_for_manager[0]
#     conn = psycopg2.connect(
#         database="test",
#         user="postgres",
#         password="12345",
#         host="localhost",
#         port="5432"
#     )
#
#     # Open a cursor to perform database operations
#     cursor = conn.cursor()
#
#     # Execute a query
#     cursor.execute("UPDATE transactions SET deleted='2021-10-10' WHERE id=1")
#
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return tokens
