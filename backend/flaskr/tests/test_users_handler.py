import pytest
import json

from flaskr.tests import get_with_auth, post, post_with_auth, flask_client, stub_user
from flaskr.db import db

from flaskr.auth import from_jwt

'''
Token acquire test
'''
def test_token_acquire(flask_client, stub_user):
    data = {
        "username": stub_user["username"],
        "password": stub_user["password"],
    }
    res = post(flask_client, "/token/", data)
    assert res.status_code == 200
    body = res.get_json()
    assert "token" in body
    token = body["token"]
    decoded = from_jwt(token)
    assert "username" in decoded
    assert decoded["username"] == data["username"]
    return token

def test_token_acquire_invalid_passwd(flask_client, stub_user):
    data = {
        "username": stub_user["username"],
        "password": "no chodź adasiu zapraszam na morenke",
    }
    res = post(flask_client, "/token/", data)
    assert res.status_code == 400

'''
Get users list
'''
def test_users_list(flask_client):
    results = get_with_auth(flask_client, "/users/")
    res = get_with_auth(flask_client, "/users/")
    assert res.status_code == 200
    body = res.get_json()
    assert "users" in body
    assert isinstance(body["users"], list)

'''
User Registration
'''
def test_register_user(flask_client, data=None):
    if data is None:
        data = {
            "username": "jajanek",
            "password": "12345678",
            "email": "morenka@sweetnight.pl"
        }

    res = post(flask_client, "/users/", data)
    assert res.status_code == 200
    result = db.users.find_one({"username":data["username"]})
    assert result != None
    assert result["email"] == data["email"]

def test_register_duplicate_user(flask_client):
    data = {
        "username": "jajanek",
        "password": "12345678",
        "email": "morenka@sweetnight.pl"
    }
    test_register_user(flask_client, data=data)
    res = post(flask_client, "/users/", data)
    assert res.status_code == 400

def test_register_user_invalid_email(flask_client):
    data = {
        "username": "jajanek",
        "password": "12345678",
        "email": "morenkasweetnight.com"
    }
    res = post(flask_client, "/users/", data)
    assert res.status_code == 400

def test_register_user_missing_field(flask_client):
    data = json.dumps({
        "username": "jajanek",
        "email": "morenka@sweetnight.pl"
    })
    res = post(flask_client, "/users/", data)
    assert res.status_code == 400

