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
    dao = UserDAO()
    user = User(user_data)
    dao.insert_one(user)

    return user


def test_confirm_invitation(clear_db, flask_client, stub_team, stub_user, invitation_link=None):
    team_dao = TeamDAO()
    team = Team(stub_team)
    team_dao.insert_one(team)
    username = stub_user.username

    if invitation_link is None:
        with app.test_client(), app.test_request_context():
            invitation_link = create_team_invitation_for_user_link(team.name, username)

    token = invitation_link.split('/')[-2]
    res = get(flask_client, "/teams/confirm_team/%s/" % token)
    assert res.status_code == 200
    assert res.get_json()["confirmation"] == "OK"

    team_from_db = team_dao.find_one_by_name(team.name)
    assert username in team_from_db.members


def create_team(flask_client, team_data, link="/teams/create_team/"):
    res = post(flask_client, link, team_data)
    assert res.status_code == 200
    assert res.get_json()["confirmation"] == "OK"


def create_team_with_missing_data(flask_client, link="/teams/create_team/"):
    data = {"name": "incorrect_team"}
    res = post(flask_client, link, data)
    assert res.status_code == 400


def create_duplicated_team(flask_client, team_data, link="/teams/create_team/"):
    create_team(flask_client, team_data, link)

    res = post(flask_client, link, team_data)
    assert res.status_code == 400


def test_create_fast_team(clear_db, flask_client, stub_team, stub_user):
    stub_team["members"].append(stub_user.username)
    create_team(flask_client, stub_team, "/teams/create_team_fast/")
    team_dao = TeamDAO()
    team_from_db = team_dao.find_one_by_name(stub_team["name"])

    assert team_from_db is not None
    assert stub_user.username in team_from_db.members


def test_create_fast_team_with_missing_data(flask_client):
    create_team_with_missing_data(flask_client, "/teams/create_team_fast/")


def test_create_duplicated_fast_teams(clear_db, flask_client, stub_team, stub_user):
    team_data = stub_team
    team_data["members"].append(stub_user.username)
    create_duplicated_team(flask_client, team_data, "/teams/create_team_fast/")


def test_create_team(clear_db, flask_client, stub_team):
    user1_data = {
        "username": "user1",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }
    user1 = User(user1_data)

    user2_data = {
        "username": "user2",
        "password": "123456789",
        "email": "stubmail2@gmail.com"
    }
    user2 = User(user2_data)

    user_dao = UserDAO()
    user_dao.insert_one(user1)
    user_dao.insert_one(user2)

    stub_team["members"].append(user1.username)
    stub_team["members"].append(user2.username)
    team_name = stub_team["name"]
    create_team(flask_client, stub_team)

    with app.test_client(), app.test_request_context():
        token1 = create_team_invitation_for_user_link(team_name, user1.username).split('/')[-2]
        token2 = create_team_invitation_for_user_link(team_name, user2.username).split('/')[-2]

    res = get(flask_client, "/teams/confirm_team/%s/" % token1)
    assert res.status_code == 200
    assert res.get_json()["confirmation"] == "OK"

    res = get(flask_client, "/teams/confirm_team/%s/" % token2)
    assert res.status_code == 200
    assert res.get_json()["confirmation"] == "OK"

    dao = TeamDAO()
    team_from_db = dao.find_one_by_name(team_name)
    members = team_from_db.members

    assert user1.username in members
    assert user2.username in members


def test_create_team_with_missing_data(flask_client):
    create_team_with_missing_data(flask_client)


def test_create_duplicated_teams(clear_db, flask_client, stub_team):
    team_data = stub_team
    user_data = {
        "username": "user",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }
    user = User(user_data)
    user_dao = UserDAO()
    user_dao.insert_one(user)

    team_data["members"].append(user.username)
    create_duplicated_team(flask_client, team_data)


def test_get_team_members_list(clear_db, flask_client, stub_team):
    team = Team(stub_team)
    team.add_user("user1")
    team.add_user("user2")
    dao = TeamDAO()
    dao.insert_one(team)

    res = get_with_auth(flask_client, "/teams/get_members/%s/" % team.name )
    assert res.status_code == 200

    members_list = res.get_json()["members"]
    assert "user1" in members_list
    assert "user2" in members_list


def test_get_non_existing_team_members_list(clear_db, flask_client):
    res = get_with_auth(flask_client, "/teams/get_members/team/")
    assert res.status_code == 400
