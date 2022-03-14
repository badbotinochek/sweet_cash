import pytest
from app import create_app
from pathlib import Path


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


# get the resources folder in the tests folder
resources = Path(__file__).parent / "resources"


EMAIL = "test1@test.com"
PHONE = '+79001234567'
PASSWORD = "1@yAndexru"


def test_edit_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Flask",
            "email": "test11@test.com",
            "phone": '+79594756685',
            "password": PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200