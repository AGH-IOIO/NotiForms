import pytest

from ..database import db
from ..database.user_dao import UserDAO
from ..model.user import User
from werkzeug.security import generate_password_hash

dao = UserDAO()


@pytest.fixture
def clear_collection():
    # clear collection before each test
    db.drop_collection("users")


@pytest.fixture
def stub_user():
    data = {
        "username": "stub_user",
        "password": "123456789",
        "email": "stubmail@gmail.com",
        "teams": []
    }
    user = User(data)
    return user


@pytest.fixture
def stub_user_2():
    data = {
        "username": "stub_user_2",
        "password": "987654321",
        "email": "stubmail2@gmail.com",
        "teams": []
    }
    user = User(data)
    return user


def test_empty_collection(clear_collection):
    users = dao.find_all_users()
    assert users == []


def test_insert_one(clear_collection, stub_user):
    dao.insert_one(stub_user)

    assert dao.does_username_or_email_exist(
        stub_user.username,
        stub_user.email
    ) is True

    user = dao.find_one_by_object(stub_user)
    assert user is not None
    assert user == stub_user

    user_2 = dao.find_one_by_id(stub_user.id)
    assert user_2 is not None
    assert user_2 == stub_user
    assert user_2 == user


def test_nonexistent_user(clear_collection):
    error_data = {
        "username": "false_user",
        "password": "not_true_password",
        "email": "nonexistent@falsemail.com",
        "teams": []
    }
    nonexistent_user = User(error_data)

    assert dao.does_username_or_email_exist(
        nonexistent_user.username,
        nonexistent_user.email
    ) is False


def test_insert_many(clear_collection, stub_user, stub_user_2):
    dao.insert_one(stub_user)
    dao.insert_one(stub_user_2)

    assert dao.does_username_or_email_exist(
        stub_user.username,
        stub_user.email
    ) is True

    assert dao.does_username_or_email_exist(
        stub_user_2.username,
        stub_user_2.email
    ) is True

    query = {"username": {"$in": [stub_user.username, stub_user_2.username]}}
    users = dao.find(query)
    assert users is not None
    assert len(users) == 2

    for user in users:
        assert user is not None
        assert user == stub_user or user == stub_user_2


def test_find_username_from_id(clear_collection, stub_user):
    dao.insert_one(stub_user)

    user = dao.find_username_from_id(stub_user.id)
    print(user)


def test_update(clear_collection, stub_user):
    dao.insert_one(stub_user)
    stub_user.password = generate_password_hash("987654321")

    query = {"_id": stub_user.id}
    update = {"$set": {"password": stub_user.password}}
    dao.update_one(query, update)

    user = dao.find_one_by_object(stub_user)
    assert user is not None
    assert user == stub_user

    stub_user.password = generate_password_hash("123456789")
    update = {"$set": {"password": stub_user.password}}
    dao.update_one_by_id(stub_user.id, update)

    user_2 = dao.find_one_by_object(stub_user)
    assert user_2 is not None
    assert user_2 == stub_user

    assert stub_user.username == user.username == user_2.username
    assert stub_user.email == user.email == user_2.email


def test_change_password(clear_collection, stub_user):
    dao.insert_one(stub_user)
    stub_user.password = generate_password_hash("987654321")

    dao.change_password(stub_user.password, username=stub_user.username)

    user = dao.find_one_by_object(stub_user)
    assert user is not None
    assert user == stub_user


def test_add_team(clear_collection, stub_user):
    dao.insert_one(stub_user)
    new_team = "new_team_name"
    dao.add_team(new_team, stub_user.username)

    user = dao.find_one_by_id(stub_user.id)
    assert user.teams is not None
    assert len(user.teams) == 1
    assert user.teams[0] == new_team


def test_remove_team(clear_collection, stub_user):
    dao.insert_one(stub_user)
    team_1 = "team_1"
    team_2 = "team_2"
    dao.add_team(team_1, stub_user.username)
    dao.add_team(team_2, stub_user.username)

    user = dao.find_one_by_id(stub_user.id)
    assert user.teams is not None
    assert len(user.teams) == 2
    assert user.teams[0] == team_1
    assert user.teams[1] == team_2

    dao.remove_team(team_1, stub_user.username)
    user = dao.find_one_by_id(stub_user.id)
    assert user.teams is not None
    assert len(user.teams) == 1
    assert user.teams[0] == team_2


def test_delete(clear_collection, stub_user, stub_user_2):
    dao.insert_one(stub_user)
    dao.insert_one(stub_user_2)

    query = {"username": stub_user.username}
    dao.delete_one(query)
    user = dao.find_one_by_id(stub_user.id)
    assert user is None

    dao.delete_one_by_id(stub_user_2.id)
    user = dao.find_one_by_id(stub_user_2.id)
    assert user is None

    users = dao.find_all_users()
    assert users == []
