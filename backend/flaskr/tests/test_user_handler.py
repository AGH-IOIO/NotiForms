import pytest
import json

from . import get_with_auth, post, post_with_auth, flask_client, \
    stub_user, clear_db
from ..database import db
from ..database.user_dao import UserDAO
from ..auth import from_jwt


# token acquire test
def test_token_acquire(clear_db, flask_client, stub_user):
    data = {
        "username": stub_user["username"],
        "password": stub_user["password"],
    }
    print("Acquiring by", data)
    res = post(flask_client, "/token/", data)
    body = res.get_json()
    print(body, flush=True)
    assert res.status_code == 200
    assert "token" in body
    token = body["token"]
    decoded = from_jwt(token)
    assert "username" in decoded
    assert decoded["username"] == data["username"]
    return token


def test_token_acquire_invalid_password(clear_db, flask_client, stub_user):
    data = {
        "username": stub_user["username"],
        "password": "van dame wali z obrotu, a segal lamie kosci",
    }
    res = post(flask_client, "/token/", data)
    assert res.status_code == 400


# get users list
def test_users_list(clear_db, flask_client):
    results = get_with_auth(flask_client, "/users/")
    print(results.get_json(), flush=True)
    assert results.status_code == 200
    body = results.get_json()
    assert "users" in body
    assert isinstance(body["users"], list)


# user registration
def test_register_user(clear_db, flask_client, data=None):
    if data is None:
        data = {
            "username": "someUser",
            "password": "123456789",
            "email": "stubmail@gmail.com"
        }

    res = post(flask_client, "/users/", data)
    print(res.get_json(), flush=True)
    assert res.status_code == 200
    dao = UserDAO()
    result = dao.find_one({"username": data["username"]})
    assert result is not None
    assert result.email == data["email"]


def test_register_duplicate_user(clear_db, flask_client):
    data = {
        "username": "someUser",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }
    test_register_user(None, flask_client, data=data)
    res = post(flask_client, "/users/", data)
    assert res.status_code == 400


def test_register_user_invalid_email(flask_client):
    data = {
        "username": "someUser",
        "password": "123456789",
        "email": "incorrectmail.com"
    }
    res = post(flask_client, "/users/", data)
    assert res.status_code == 400


def test_register_user_missing_field(flask_client):
    data = json.dumps({
        "username": "someUser",
        "email": "stubmail@gmail.com"
    })
    res = post(flask_client, "/users/", data)
    assert res.status_code == 400

