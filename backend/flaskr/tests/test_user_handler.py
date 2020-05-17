import pytest
import json

from . import get_with_auth, post, post_with_auth, flask_client, \
    stub_user, clear_db, get, app
from ..database.user_dao import UserDAO
from ..database.unconfirmed_user_dao import UnconfirmedUserDAO
from ..database.team_dao import TeamDAO
from ..auth import from_jwt
from ..model.user import User
from ..model.team import Team
from ..model.unconfirmed_user import UnconfirmedUser
from ..model.utils import create_team_invitation_for_user_link, \
    create_user_registration_link


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
    dao = UnconfirmedUserDAO()
    result = dao.find_one({"user.username": data["username"]})
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


def test_confirm_user(clear_db, flask_client):
    user_data = {
        "username": "someUser",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }

    with app.test_client(), app.test_request_context():
        data = {
            "link": create_user_registration_link(user_data["username"]),
            "user": user_data
        }

    user = UnconfirmedUser(data)
    unconfirmed_dao = UnconfirmedUserDAO()
    unconfirmed_dao.insert_one(user)

    token = user.link.split('/')[-2]
    res = get(flask_client, "/users/confirm/%s/" % token)
    assert res.status_code == 200
    assert res.get_json()["confirmation"] == "OK"

    dao = UserDAO()
    user_from_db = dao.find_one({"username": data["user"]["username"]})
    assert user_from_db is not None


def test_confirmed_user_confirm(clear_db, flask_client):
    user_data = {
        "username": "someUser",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }

    with app.test_client(), app.test_request_context():
        data = {
            "link": create_user_registration_link(user_data["username"]),
            "user": user_data
        }

    user = UnconfirmedUser(data)
    unconfirmed_dao = UnconfirmedUserDAO()
    unconfirmed_dao.insert_one(user)

    token = user.link.split('/')[-2]
    res = get(flask_client, "/users/confirm/%s/" % token)
    assert res.status_code == 200
    assert res.get_json()["confirmation"] == "OK"

    res = get(flask_client, "/users/confirm/%s/" % token)
    assert res.status_code == 200
    assert res.get_json()["confirmation"] == "Error"


def test_confirm_invitation(clear_db, flask_client):
    team_data = {
        "name": "test_team",
        "users": []
    }
    team = Team(team_data)

    user_data = {
        "username": "new_user",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }
    user = User(user_data)

    user_dao = UserDAO()
    team_dao = TeamDAO()

    user_dao.insert_one(user)
    team_dao.insert_one(team)

    with app.test_client(), app.test_request_context():
        invitation_link = create_team_invitation_for_user_link(team.name,
                                                               user.username)

    token = invitation_link.split('/')[-2]
    res = get(flask_client, "/teams/confirm_team/%s/" % token)
    assert res.status_code == 200
    assert res.get_json()["confirmation"] == "OK"

    team_from_db = team_dao.find_one_by_name(team.name)
    assert user.username in team_from_db.members


def test_get_user_teams(clear_db, flask_client):
    user_data = {
        "username": "new_user",
        "password": "123456789",
        "email": "stubmail@gmail.com",
        "teams": ["test_team"]
    }
    user = User(user_data)

    team_data = {
        "name": "test_team",
        "users": [user.username]
    }
    team = Team(team_data)

    user_dao = UserDAO()
    team_dao = TeamDAO()

    user_dao.insert_one(user)
    team_dao.insert_one(team)

    res = get_with_auth(flask_client, "/users/get_teams/" + user.username + "/")
    assert res.status_code == 200
    assert team.name in res.get_json()["teams"]


def test_get_user_teams_with_no_teams(clear_db, flask_client, stub_user):
    user = User(stub_user)
    user_dao = UserDAO()
    user_dao.insert_one(user)

    res = get_with_auth(flask_client, "/users/get_teams/" + user.username + "/")
    assert res.status_code == 200
    assert len(res.get_json()["teams"]) == 0
