from tests.test_config import TestConfig

HOST = TestConfig.HOST


'''
TEST CREATING EVENT
'''


def test_create_event_success(client, get_token):
    """Ожидаемый результат - Успех. Создание нового мероприятия"""
    tokens = get_token[0]
    user_ids = get_token[1]
    response = client.post(
        HOST + "/api/v1/events",
        json={
            "name": "Событие",
            "start": "2022-02-01T04:25:03Z",
            "end": "2022-02-01T04:25:03Z",
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
    assert response['participants_info']['participants'][0]["user_id"] == user_ids[0]
    assert "role" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["role"] == "Manager"
    assert "is_accepted" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["is_accepted"] is True


def test_create_event_without_valid_token(client):
    response = client.post(
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
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "msg": "Missing Authorization Header"
    }


def test_create_event_without_body(client, get_token):
    tokens = get_token[0]
    response = client.post(
        HOST + "/api/v1/events",
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_create_event_without_required_params(client, get_token):
    tokens = get_token[0]
    response = client.post(
        HOST + "/api/v1/events",
        json={},
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('name',) required",
        "status": 400
    }


def test_create_event_with_wrong_types_for_params(client, get_token):
    tokens = get_token[0]
    response = client.post(
        HOST + "/api/v1/events",
        json={
            "name": 1,
            "start": 1.5,
            "end": True,
            "description": -1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('name', 'start', 'end', 'description')",
        "status": 400
    }


'''
TEST GETTING EVENTS
'''


def test_get_events_for_manager_success(client, create_events):
    tokens = create_events[0]
    user_ids = create_events[1]
    event_ids = create_events[2]
    response = client.get(
        HOST + "/api/v1/events?ids=" + str(event_ids[0]),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
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
    assert response['participants_info']['participants'][0]["user_id"] == user_ids[0]
    assert "role" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["role"] == "Manager"
    assert "is_accepted" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["is_accepted"] is True


def test_get_events_for_not_verified_partner_success(client, create_participant):
    tokens = create_participant[0]
    user_ids = create_participant[1]
    event_ids = create_participant[2]
    response = client.get(
        HOST + "/api/v1/events?ids=" + str(event_ids[0]),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
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
    assert response['participants_info']["total"] == 2
    assert "your_role" in response['participants_info']
    assert response['participants_info']["your_role"] == "Partner"
    assert "is_accepted" in response['participants_info']
    assert response['participants_info']["is_accepted"] is False
    assert "participants" in response['participants_info']
    assert len(response['participants_info']['participants']) == 2
    assert "id" in response['participants_info']['participants'][0]
    assert "created_at" in response['participants_info']['participants'][0]
    assert "updated_at" in response['participants_info']['participants'][0]
    assert "user_id" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["user_id"] == user_ids[0]
    assert "role" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["role"] == "Manager"
    assert "is_accepted" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["is_accepted"] is True


def test_get_events_for_not_verified_observer_success(client, create_participant):
    tokens = create_participant[0]
    user_ids = create_participant[1]
    event_ids = create_participant[2]
    response = client.get(
        HOST + "/api/v1/events?ids=" + str(event_ids[6]),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
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
    assert response['participants_info']["total"] == 2
    assert "your_role" in response['participants_info']
    assert response['participants_info']["your_role"] == "Observer"
    assert "is_accepted" in response['participants_info']
    assert response['participants_info']["is_accepted"] is False
    assert "participants" in response['participants_info']
    assert len(response['participants_info']['participants']) == 2
    assert "id" in response['participants_info']['participants'][0]
    assert "created_at" in response['participants_info']['participants'][0]
    assert "updated_at" in response['participants_info']['participants'][0]
    assert "user_id" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["user_id"] == user_ids[1]
    assert "role" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["role"] == "Manager"
    assert "is_accepted" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["is_accepted"] is True


def test_get_events_for_verified_partner_success(client, confirm_event):
    tokens = confirm_event[0]
    user_ids = confirm_event[1]
    event_ids = confirm_event[2]
    response = client.get(
        HOST + "/api/v1/events?ids=" + str(event_ids[0]),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
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
    assert response['participants_info']["total"] == 2
    assert "your_role" in response['participants_info']
    assert response['participants_info']["your_role"] == "Partner"
    assert "is_accepted" in response['participants_info']
    assert response['participants_info']["is_accepted"] is True
    assert "participants" in response['participants_info']
    assert "id" in response['participants_info']['participants'][0]
    assert "created_at" in response['participants_info']['participants'][0]
    assert "updated_at" in response['participants_info']['participants'][0]
    assert "user_id" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["user_id"] == user_ids[0]
    assert "role" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["role"] == "Manager"
    assert "is_accepted" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["is_accepted"] is True


def test_get_events_for_verified_observer_success(client, confirm_event):
    tokens = confirm_event[0]
    user_ids = confirm_event[1]
    event_ids = confirm_event[2]
    response = client.get(
        HOST + "/api/v1/events?ids=" + str(event_ids[6]),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
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
    assert response['participants_info']["total"] == 2
    assert "your_role" in response['participants_info']
    assert response['participants_info']["your_role"] == "Observer"
    assert "is_accepted" in response['participants_info']
    assert response['participants_info']["is_accepted"] is True
    assert "participants" in response['participants_info']
    assert "id" in response['participants_info']['participants'][0]
    assert "created_at" in response['participants_info']['participants'][0]
    assert "updated_at" in response['participants_info']['participants'][0]
    assert "user_id" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["user_id"] == user_ids[1]
    assert "role" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["role"] == "Manager"
    assert "is_accepted" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["is_accepted"] is True


def test_get_event_without_valid_token(client, create_events):
    event_ids = create_events[2]
    response = client.get(
        HOST + "/api/v1/events?ids=" + str(event_ids[0]),
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "msg": "Missing Authorization Header"
    }


def test_get_event_without_required_params(client, create_events):
    tokens = create_events[0]
    response = client.get(
        HOST + "/api/v1/events",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 0


def test_get_null_events(client, create_events):
    tokens = create_events[0]
    event_ids = create_events[2]
    response = client.get(
        HOST + "/api/v1/events?ids=" + str(event_ids[0]),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[1]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Participant for user 2 not found"
    }


def test_get_events_without_ids(client, create_events):
    tokens = create_events[0]
    response = client.get(
        HOST + "/api/v1/events?ids=" + str(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 0


'''
TEST GETTING EVENTS BY FILTER
'''


def test_get_events_manager_success(client, create_events):
    tokens = create_events[0]
    response = client.get(
        HOST + "/api/v1/events/by_filter?role=Manager",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
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


def test_get_events_by_filter_not_verified_participant_success(client, create_participant):
    tokens = create_participant[0]
    response = client.get(
        HOST + "/api/v1/events/by_filter?accepted=False",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 5
    for i in range(4):
        assert response[i]['participants_info']["is_accepted"] is False


def test_get_events_by_filter_verified_partner_success(client, confirm_event):
    tokens = confirm_event[0]
    response = client.get(
        HOST + "/api/v1/events/by_filter?accepted=True&role=Partner",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 1
    assert response[0]['participants_info']["is_accepted"] is True
    assert response[0]['participants_info']["your_role"] == "Partner"


def test_get_events_by_filter_verified_observer_success(client, confirm_event):
    tokens = confirm_event[0]
    response = client.get(
        HOST + "/api/v1/events/by_filter?accepted=False&role=Observer",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 1
    assert response[0]['participants_info']["is_accepted"] is True
    assert response[0]['participants_info']["your_role"] == "Observer"


def test__get_events_by_filter_without_valid_token(client):
    response = client.get(
        HOST + "/api/v1/events/by_filter?role=Manager",
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_get_events_by_filter_without_required_params(client, create_events):
    tokens = create_events[0]
    response = client.get(
        HOST + "/api/v1/events/by_filter?role",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) > 0


def test_get_events_by_filter_null_events(client, create_events):
    tokens = create_events[0]
    response = client.get(
        HOST + "/api/v1/events/by_filter?role=Manager",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert len(response) == 0


'''
TEST UPDATING EVENT
'''


def test_update_event_without_participant_success(client, create_events):
    tokens = create_events[0]
    user_ids = create_events[1]
    event_ids = create_events[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]),
        json={
            "name": "Событие 1",
            "start": "2022-02-01T04:25:03Z",
            "end": "2022-02-01T04:25:03Z",
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
    assert response['participants_info']['participants'][0]["user_id"] == user_ids[0]
    assert "role" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["role"] == "Manager"
    assert "is_accepted" in response['participants_info']['participants'][0]
    assert response['participants_info']['participants'][0]["is_accepted"] is True


def test_update_event_without_valid_token(client, create_events):
    event_ids = create_events[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]),
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


def test_update_event_without_body(client, create_events):
    tokens = create_events[0]
    event_ids = create_events[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]),
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_update_event_without_required_params(client, create_events):
    tokens = create_events[0]
    event_ids = create_events[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]),
        json={},
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('name',) required",
        "status": 400
    }


def test_update_event_with_wrong_types_for_params(client, create_events):
    tokens = create_events[0]
    event_ids = create_events[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]),
        json={
            "name": 1,
            "start": 1.5,
            "end": True,
            "description": -1
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('name', 'start', 'end', 'description')",
        "status": 400
    }


def test_update_event_not_verified_partner_error(client, create_participant):
    tokens = create_participant[0]
    event_ids = create_participant[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]),
        json={
            "name": "Событие 1",
            "start": "2022-02-01T04:25:03Z",
            "end": "2022-02-01T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Accepted user 3 not found in event 1",
    }


def test_update_event_verified_partner_error(client, confirm_event):
    tokens = confirm_event[0]
    event_ids = confirm_event[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]),
        json={
            "name": "Событие 1",
            "start": "2022-02-01T04:25:03Z",
            "end": "2022-02-01T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "User 3 with Manager not found in event 1",
    }


def test_update_event_not_verified_observer_error(client, create_participant):
    tokens = create_participant[0]
    event_ids = create_participant[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[6]),
        json={
            "name": "Событие 1",
            "start": "2022-02-01T04:25:03Z",
            "end": "2022-02-01T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Accepted user 4 not found in event 7",
    }


def test_update_event_verified_observer_error(client, confirm_event):
    tokens = confirm_event[0]
    event_ids = confirm_event[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[6]),
        json={
            "name": "Событие 1",
            "start": "2022-02-01T04:25:03Z",
            "end": "2022-02-01T04:25:03Z",
            "description": "description"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[3]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "User 4 with Manager not found in event 7",
    }


'''
TEST CREATING PARTICIPANT
'''


def test_create_participant_success(client, create_events):
    tokens = create_events[0]
    user_ids = create_events[1]
    event_ids = create_events[2]
    response = client.post(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant",
        json={
            "user_id": user_ids[1],
            "role": "Partner"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response
    assert "user_id" in response
    assert response["user_id"] == user_ids[1]
    assert "role" in response
    assert response["role"] == "Partner"
    assert "is_accepted" in response
    assert response["is_accepted"] is False


def test_create_participant_without_valid_token(client, create_events):
    user_ids = create_events[1]
    event_ids = create_events[2]
    response = client.post(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant",
        json={
            "user_id": user_ids[1],
            "role": "Partner"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_create_participant_without_body(client, create_events):
    tokens = create_events[0]
    event_ids = create_events[2]
    response = client.post(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant",
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_create_participant_without_required_params(client, create_events):
    tokens = create_events[0]
    event_ids = create_events[2]
    response = client.post(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant",
        json={},
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('user_id', 'role') required",
        "status": 400
    }


def test_create_participant_with_wrong_types_for_params(client, create_events):
    tokens = create_events[0]
    event_ids = create_events[2]
    response = client.post(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant",
        json={
            "user_id": True,
            "role": 2
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('user_id', 'role')",
        "status": 400
    }


def test_create_participant_error(client, create_events):
    tokens = create_events[0]
    user_ids = create_events[1]
    event_ids = create_events[2]
    response = client.post(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant",
        json={
            "user_id": user_ids[1],
            "role": "Partner"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Participant for user 3 not found",
    }


'''
TEST UPDATING PARTICIPANT
'''


def test_update_not_verified_participant_success(client, create_participant):
    tokens = create_participant[0]
    user_ids = create_participant[1]
    event_ids = create_participant[2]
    participant_ids = create_participant[3]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/" + str(participant_ids[0]),
        json={
            "role": "Manager"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response = response.get_json()
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response
    assert "user_id" in response
    assert response["user_id"] == user_ids[2]
    assert "role" in response
    assert response["role"] == "Manager"
    assert "is_accepted" in response
    assert response["is_accepted"] is False


def test_update_verified_participant_error(client, confirm_event):
    tokens = confirm_event[0]
    event_ids = confirm_event[2]
    participant_ids = confirm_event[3]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/" + str(participant_ids[0]),
        json={
            "role": "Observer"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 409
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Conflict",
        "message": "You cannot update your participant",
    }


def test_update_participant_myself_error(client, create_participant):
    tokens = create_participant[0]
    event_ids = create_participant[2]
    participant_ids = create_participant[3]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/" + str(participant_ids[0]),
        json={
            "role": "Observer"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "Accepted user 3 not found in event 1",
    }


def test_update_verified_participant_myself_error(client, confirm_event):
    tokens = confirm_event[0]
    event_ids = confirm_event[2]
    participant_ids = confirm_event[3]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/" + str(participant_ids[0]),
        json={
            "role": "Observer"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error": "Not found",
        "message": "User 3 with Manager not found in event 1",
    }


def test_update_participant_without_valid_token(client, create_participant):
    event_ids = create_participant[2]
    participant_ids = create_participant[3]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/" + str(participant_ids[0]),
        json={
            "role": "Observer"
        },
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


def test_update_participant_without_body(client, create_participant):
    tokens = create_participant[0]
    event_ids = create_participant[2]
    participant_ids = create_participant[3]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/" + str(participant_ids[0]),
        headers={"Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Json required",
        "status": 400
    }


def test_update_participant_without_required_params(client, create_participant):
    tokens = create_participant[0]
    event_ids = create_participant[2]
    participant_ids = create_participant[3]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/" + str(participant_ids[0]),
        json={},
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Params ('role',) required",
        "status": 400
    }


def test_update_participant_with_wrong_types_for_params(client, create_participant):
    tokens = create_participant[0]
    event_ids = create_participant[2]
    participant_ids = create_participant[3]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/" + str(participant_ids[0]),
        json={
            "role": 2
        },
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[0]}
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == {
        "error_code": "bad-params",
        "message": "Invalid type for params ('role',)",
        "status": 400
    }


'''
TEST CONFIRMATION EVENT
'''


def test_confirm_event_success(client, create_participant):
    tokens = create_participant[0]
    event_ids = create_participant[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/confirm",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


def test_confirm_event_without_valid_token(client, create_participant):
    tokens = create_participant[0]
    event_ids = create_participant[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/confirm",
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401


'''
TEST REJECTION EVENT
'''


def test_reject_event_success(client, create_participant):
    tokens = create_participant[0]
    event_ids = create_participant[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/reject",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + tokens[2]}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


def test_reject_event_without_valid_token(client, create_participant):
    event_ids = create_participant[2]
    response = client.put(
        HOST + "/api/v1/events/" + str(event_ids[0]) + "/participant/reject",
        headers={"Content-Type": "application/json",
                 "Authorization": ""}
    )
    assert response.status_code == 401
