import pytest

from ..tests import stub_user
from ..database import db
from ..database.user_dao import UserDAO
from ..model.user import User

dao = UserDAO()


@pytest.fixture
def stub_user():
    data = {
        "username": "stubUser",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }
    new_user = User(**data)
    return new_user


@pytest.fixture
def clear_collection():
    # clear collection before each test
    db.drop_collection("users")


def test_empty_collection(clear_collection):
    users = dao.find_all_users()
    assert users == []


def test_insert_one(clear_collection, stub_user):
    dao.insert_one(stub_user)
    users = dao.find_all_users()
    print(stub_user)
    for user in users:
        print(user)
    user = dao.find_one_by_user_object(stub_user)
    assert user is not None
    assert user == stub_user
