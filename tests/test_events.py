import pytest
import requests

HOST = 'http://127.0.0.1:5000'
user_email = (lambda n: f'test{n}@test.com')
PASSWORD = "1@yAndexru"

USER_IDS = []
TOKENS = []

for i in range(1, 4):
    login_response = requests.post(
        HOST + "/api/v1/auth/login",
        json={
            "email": user_email(i),
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    ).json()

    refresh_token = login_response["refresh_token"]
    USER_IDS.append(login_response["user_id"])

    token = requests.post(
        HOST + "/api/v1/auth/token",
        json={
            "refresh_token": refresh_token
        },
        headers={"Content-Type": "application/json"}
    ).json()["token"]
    TOKENS.append(token)

EVENT_ID = ''
PARTICIPANT_ID = ''

'''
TEST CREATING EVENT
'''


def test_create_event_success():
    global EVENT_ID
    response = requests.post(
        HOST + "/api/v1/events",
        json={
            "name": "Событие",
            "start": "2022-02-01T04:25:03Z",
            "end": "2022-02-01T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.json()
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response
    assert "name" in response
    assert "description" in response
    assert "start" in response
    assert "end" in response
    assert "participants_info" in response
    assert "total" in response['participants_info']
    assert response['participants_info']["total"] == 1
    assert "your_role" in response['participants_info']
    assert response['participants_info']["your_role"] == "Manager"
    assert "is_accepted" in response['participants_info']
    assert response['participants_info']["is_accepted"] is True
    assert "participants" in response['participants_info']
    assert len(response['participants_info']['participants']) == 1
    assert "id" in response['participants_info']['participants'][0]
    assert "created_at" in response['participants_info']['participants'][0]
    assert "updated_at" in response['participants_info']['participants'][0]
    assert "user_id" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["user_id"] == USER_IDS[0]
    assert "role" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["role"] == "Manager"
    assert "is_accepted" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["is_accepted"] is True
    EVENT_ID = response["id"]


def test_create_event_without_valid_token():
    response = requests.post(
        HOST + "/api/v1/events",
        json={
            "name": "Событие",
            "start": "2022-02-01T04:25:03Z",
            "end": "2022-02-01T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_create_event_without_body():
    response = requests.post(
        HOST + "/api/v1/events",
        headers={"Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_create_event_without_required_params():
    response = requests.post(
        HOST + "/api/v1/events",
        json={},
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Params ('name',) required",
        "status": 400
    }


def test_create_event_with_wrong_types_for_params():
    response = requests.post(
        HOST + "/api/v1/events",
        json={
            "name": 1,
            "start": 1.5,
            "end": True,
            "description": -1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('name', 'start', 'end', 'description')",
        "status": 400
    }


'''
TEST GETTING EVENTS
'''


def test_get_events_success():
    response = requests.get(
        HOST + "/api/v1/events?ids=" + str(EVENT_ID),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.json()
    assert len(response) == 1
    response = response[0]
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response
    assert "name" in response
    assert "description" in response
    assert "start" in response
    assert "end" in response
    assert "participants_info" in response
    assert "total" in response['participants_info']
    assert response['participants_info']["total"] == 1
    assert "your_role" in response['participants_info']
    assert response['participants_info']["your_role"] == "Manager"
    assert "is_accepted" in response['participants_info']
    assert response['participants_info']["is_accepted"] is True
    assert "participants" in response['participants_info']
    assert len(response['participants_info']['participants']) == 1
    assert "id" in response['participants_info']['participants'][0]
    assert "created_at" in response['participants_info']['participants'][0]
    assert "updated_at" in response['participants_info']['participants'][0]
    assert "user_id" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["user_id"] == USER_IDS[0]
    assert "role" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["role"] == "Manager"
    assert "is_accepted" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["is_accepted"] is True


def test_get_event_without_valid_token():
    response = requests.get(
        HOST + "/api/v1/events?ids=" + str(EVENT_ID),
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_get_event_without_required_params():
    response = requests.get(
        HOST + "/api/v1/events",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.json()
    assert len(response) == 0


'''
TEST GETTING EVENTS BY FILTER
'''


def test_get_events_by_filter_success():
    response = requests.get(
        HOST + "/api/v1/events/by_filter?role=Manager",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.json()
    assert len(response) > 0
    response = response[0]
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response
    assert "name" in response
    assert "description" in response
    assert "start" in response
    assert "end" in response
    assert "participants_info" in response
    assert "total" in response['participants_info']
    assert response['participants_info']["total"] > 0
    assert "your_role" in response['participants_info']
    assert response['participants_info']["your_role"] == "Manager"
    assert "is_accepted" in response['participants_info']
    assert response['participants_info']["is_accepted"] is True
    assert "participants" in response['participants_info']
    assert len(response['participants_info']['participants']) > 0


def test__get_events_by_filter_without_valid_token():
    response = requests.get(
        HOST + "/api/v1/events/by_filter?role=Manager",
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_get_events_by_filter_without_required_params():
    response = requests.get(
        HOST + "/api/v1/events/by_filter?role=Manager",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.json()
    assert len(response) > 0


'''
TEST UPDATING EVENT
'''


def test_update_event_success():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID),
        json={
            "name": "Событие 1",
            "start": "2022-02-01T04:25:03Z",
            "end": "2022-02-01T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.json()
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response
    assert "name" in response
    assert response["name"] == "Событие 1"
    assert "description" in response
    assert "start" in response
    assert "end" in response
    assert "participants_info" in response
    assert "total" in response['participants_info']
    assert response['participants_info']["total"] == 1
    assert "your_role" in response['participants_info']
    assert response['participants_info']["your_role"] == "Manager"
    assert "is_accepted" in response['participants_info']
    assert response['participants_info']["is_accepted"] is True
    assert "participants" in response['participants_info']
    assert len(response['participants_info']['participants']) == 1
    assert "id" in response['participants_info']['participants'][0]
    assert "created_at" in response['participants_info']['participants'][0]
    assert "updated_at" in response['participants_info']['participants'][0]
    assert "user_id" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["user_id"] == USER_IDS[0]
    assert "role" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["role"] == "Manager"
    assert "is_accepted" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["is_accepted"] is True


def test_update_event_without_valid_token():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID),
        json={
            "name": "Событие 1",
            "start": "2022-02-01T04:25:03Z",
            "end": "2022-02-01T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_update_event_without_body():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID),
        headers={"Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_update_event_without_required_params():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID),
        json={},
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Params ('name',) required",
        "status": 400
    }


def test_update_event_with_wrong_types_for_params():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID),
        json={
            "name": 1,
            "start": 1.5,
            "end": True,
            "description": -1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('name', 'start', 'end', 'description')",
        "status": 400
    }


'''
TEST CREATING PARTICIPANT
'''


def test_create_participant_success():
    global PARTICIPANT_ID
    response = requests.post(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant",
        json={
            "user_id": USER_IDS[1],
            "role": "Partner"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.json()
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response
    assert "user_id" in response
    assert response["user_id"] == USER_IDS[1]
    assert "role" in response
    assert response["role"] == "Partner"
    assert "is_accepted" in response
    assert response["is_accepted"] is False
    PARTICIPANT_ID = response["id"]


def test_create_participant_without_valid_token():
    response = requests.post(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant",
        json={
            "user_id": USER_IDS[1],
            "role": "Partner"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_create_participant_without_body():
    response = requests.post(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant",
        headers={"Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_create_participant_without_required_params():
    response = requests.post(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant",
        json={},
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Params ('user_id', 'role') required",
        "status": 400
    }


def test_create_participant_with_wrong_types_for_params():
    response = requests.post(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant",
        json={
            "user_id": True,
            "role": 2
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('user_id', 'role')",
        "status": 400
    }


'''
TEST UPDATING PARTICIPANT
'''


def test_update_participant_success():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant/" + str(PARTICIPANT_ID),
        json={
            "role": "Observer"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.json()
    assert "id" in response
    assert response["id"] == PARTICIPANT_ID
    assert "created_at" in response
    assert "updated_at" in response
    assert "user_id" in response
    assert response["user_id"] == USER_IDS[1]
    assert "role" in response
    assert response["role"] == "Observer"
    assert "is_accepted" in response
    assert response["is_accepted"] is False


def test_update_participant_without_valid_token():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant/" + str(PARTICIPANT_ID),
        json={
            "role": "Observer"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_update_participant_without_body():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant/" + str(PARTICIPANT_ID),
        headers={"Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_update_participant_without_required_params():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant/" + str(PARTICIPANT_ID),
        json={},
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Params ('role',) required",
        "status": 400
    }


def test_update_participant_with_wrong_types_for_params():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant/" + str(PARTICIPANT_ID),
        json={
            "role": 2
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('role',)",
        "status": 400
    }


'''
TEST CONFIRMATION EVENT
'''


def test_confirm_event_success():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant/confirm",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[1]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


def test_confirm_event_without_valid_token():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant/confirm",
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


'''
TEST REJECTION EVENT
'''


def test_reject_event_success():
    # Create a new participant
    requests.post(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant",
        json={
            "user_id": USER_IDS[2],
            "role": "Partner"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[0]}
    )

    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant/reject",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + TOKENS[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


def test_reject_event_without_valid_token():
    response = requests.put(
        HOST + "/api/v1/events/" + str(EVENT_ID) + "/participant/reject",
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401
