import pytest

from ..database import db
from ..database.team_dao import TeamDAO
from ..model.team import Team

dao = TeamDAO()


@pytest.fixture
def clear_collection():
    # clear collection before each test
    db.drop_collection("teams")


@pytest.fixture
def stub_team():
    data = {
        "name": "stub_team",
        "users": []
    }
    team = Team(data)
    return team


@pytest.fixture
def stub_team_2():
    data = {
        "name": "stub_team_2",
        "users": ["user_2"]
    }
    team = Team(data)
    return team


def test_insert_one(clear_collection, stub_team):
    dao.insert_one(stub_team)

    assert dao.does_team_name_exist(stub_team.name)

    team = dao.find_one_by_object(stub_team)
    assert team is not None
    assert team == stub_team

    team_2 = dao.find_one_by_id(stub_team.id)
    assert team_2 is not None
    assert team_2 == stub_team
    assert team_2 == team


def test_nonexistent_user(clear_collection):
    error_data = {
        "name": "false_team",
        "users": []
    }
    nonexistent_team = Team(error_data)

    assert dao.does_team_name_exist(nonexistent_team.name) is False


def test_insert_many(clear_collection, stub_team, stub_team_2):
    dao.insert_one(stub_team)
    dao.insert_one(stub_team_2)

    assert dao.does_team_name_exist(stub_team.name) is True
    assert dao.does_team_name_exist(stub_team_2.name) is True

    teams = dao.find_all_teams()
    assert teams is not None
    assert len(teams) == 2

    for team in teams:
        assert team is not None
        assert team == stub_team or team == stub_team_2


def test_update(clear_collection, stub_team):
    dao.insert_one(stub_team)

    old_name = stub_team.name
    new_name = "new_name"
    available = dao.is_name_available(new_name)
    assert available is True

    stub_team.name = new_name

    query = {"_id": stub_team.id}
    update = {"$set": {"name": new_name}}
    dao.update_one(query, update)

    team = dao.find_one_by_object(stub_team)
    assert team is not None
    assert team == stub_team

    assert dao.is_name_available(old_name) is True


def test_add_user(clear_collection, stub_team):
    dao.insert_one(stub_team)
    new_user = "username"
    dao.add_user(new_user, stub_team.name)

    team = dao.find_one_by_id(stub_team.id)
    assert team.members is not None
    assert len(team.members) == 1
    assert team.members[0] == new_user


def test_remove_user(clear_collection, stub_team):
    dao.insert_one(stub_team)
    user_1 = "user_1"
    user_2 = "user_2"
    dao.add_user(user_1, stub_team.name)
    dao.add_user(user_2, stub_team.name)

    team = dao.find_one_by_id(stub_team.id)
    assert team.members is not None
    assert len(team.members) == 2
    assert team.members[0] == user_1
    assert team.members[1] == user_2

    dao.remove_user(user_1, stub_team.name)
    team = dao.find_one_by_id(stub_team.id)
    assert team.members is not None
    assert len(team.members) == 1
    assert team.members[0] == user_2


def test_find_users_from_team(clear_collection, stub_team):
    dao.insert_one(stub_team)
    users = dao.find_users_from_team(stub_team.name)
    assert stub_team.members == users
