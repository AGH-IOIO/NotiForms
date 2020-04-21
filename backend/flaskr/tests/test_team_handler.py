import pytest

from . import get_with_auth, post, post_with_auth, flask_client, \
    stub_user, clear_db, get, app
from ..database import db
from ..database.user_dao import UserDAO
from ..database.team_dao import TeamDAO
from ..model.user import User
from ..model.team import Team
from ..model.utils import create_team_invitation_for_user_link


@pytest.fixture
def stub_team():
    data = {
        "name": "stub_team",
        "members": []
    }
    return data


@pytest.fixture
def stub_user():
    user_data = {
        "username": "new_user",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }
    return user_data


def test_confirm_invitation(clear_db, flask_client, stub_team, stub_user):
    user_dao = UserDAO()
    team_dao = TeamDAO()

    team = Team(stub_team)
    user = User(stub_user)

    user_dao.insert_one(user)
    team_dao.insert_one(team)

    with app.test_client(), app.test_request_context():
        invitation_link = create_team_invitation_for_user_link(team, user.username)

    token = invitation_link.split('/')[-1]
    res = get(flask_client, "/teams/confirm_team/" + token)
    assert res.status_code == 200
    assert res.get_json()["confirmation"] == "OK"

    team_from_db = team_dao.find_one_by_name(team.name)
    assert user.username in team_from_db.members


def test_create_team(clear_db, flask_client, stub_team, stub_user, team_data=None):
    if team_data is None:
        team_data = stub_team
        team_data["members"].append(stub_user["username"])

    res = post(flask_client, "/teams/create_team/", team_data)
    assert res.status_code == 200
    assert res.get_json()["confirmation"] == "OK"

    team_dao = TeamDAO()
    team_from_db = team_dao.find_one_by_name(team_data["name"])
    username = team_data["members"][0]
    assert team_from_db is not None
    assert username in team_from_db.members


def test_create_team_with_missing_data(clear_db, flask_client):
    data = {"name": "incorrect_team"}
    res = post(flask_client, "/teams/create_team/", data)
    assert res.status_code == 400


def test_create_duplicated_team(clear_db, flask_client, stub_team, stub_user):
    stub_team["members"].append(stub_user["username"])
    test_create_team(None, flask_client, stub_team, stub_user, stub_team)

    res = post(flask_client, "/teams/create_team/", stub_team)
    assert res.status_code == 400


def test_get_team_members_list(clear_db, flask_client, stub_team):
    team = Team(stub_team)
    team.add_user("user1")
    team.add_user("user2")
    dao = TeamDAO()
    dao.insert_one(team)

    res = get_with_auth(flask_client, "/teams/get_members/" + team.name)
    assert res.status_code == 200

    members_list = res.get_json()["members"]
    assert "user1" in members_list
    assert "user2" in members_list


def test_get_non_existing_team_members_list(clear_db, flask_client):
    res = get_with_auth(flask_client, "/teams/get_members/team")
    assert res.status_code == 400
