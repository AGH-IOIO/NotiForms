import os
import json
import pytest

from flaskr import app
from flaskr.db import conn, db
from flaskr.auth import as_jwt

@pytest.fixture
def flask_client():
    # This gives better error messages.
    app.config["TESTING"] = True

    # Clear database before each test
    conn.drop_database(os.environ["DB_NAME"])

    # Return flask client
    with app.test_client() as client:
        yield client

@pytest.fixture
def stub_user():
    # TODO: Replace with DAO function call
    new_user = {
        "email": "morenka@sweetnight.pl",
        "password": "123456789",
        "username": "pietrek-kogucik"
    }
    db.users.insert_one(new_user)
    return new_user


def auth_token(username):
    return as_jwt({"username": username})

def get(client, path, headers = {}):
    return client.get(path, headers=headers)

def get_with_auth(client, path, username="pietrek"):
    headers = {
        "Authorization" : auth_token(path)
    }
    return get(client, path, headers=headers)

def post(client, path, data, headers = {}):
    return client.post(
        path,
        data=json.dumps(data),
        content_type="application/json",
        headers=headers
    )

def post_with_auth(client, path, data, username="pietrek"):
    # TODO: Add user with that username into DB.
    headers = {
        "Authorization" : auth_token(path)
    }
    return post(client, path, data, headers)
