import os
import json
import pytest

from ..auth import as_jwt
from ..database import connection
from ..database.user_dao import UserDAO
from ...flaskr import app
from ..model.user import User


@pytest.fixture
def flask_client():
    # This gives better error messages.
    app.config["TESTING"] = True

    # Return flask client
    with app.test_client() as client:
        yield client


@pytest.fixture
def clear_db():
    # clear the entire database
    connection.drop_database(os.environ["DB_NAME"])


@pytest.fixture
def stub_user():
    data = {
        "username": "stubUser",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }
    new_user = User(dict(data))
    dao = UserDAO()
    dao.insert_one(new_user)
    return data


def auth_token(username):
    return as_jwt({"username": username})


def get(client, path, headers=None):
    if headers is None:
        headers = {}
    return client.get(path, headers=headers)


def get_with_auth(client, path, username="pietrek"):
    headers = {
        "Authorization" : auth_token(path)
    }
    return get(client, path, headers=headers)


def post(client, path, data={}, headers=None):
    if headers is None:
        headers = {}
    return client.post(
        path,
        data=json.dumps(data),
        content_type="application/json",
        headers=headers
    )


def post_with_auth(client, path, data, username="pietrek"):
    # TODO: Add user with that username into DB.
    headers = {
        "Authorization": auth_token(path)
    }
    return post(client, path, data, headers)
