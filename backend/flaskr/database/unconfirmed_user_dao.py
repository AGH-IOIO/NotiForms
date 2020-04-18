from . import db
from ..model.unconfirmed_user import UnconfirmedUser
from ..model.user import User
from .user_dao import UserDAO as ConfirmedUserDAO


# TODO: then the database will be properly created, set TTL (index with TTL) on this collection
class UnconfirmedUserDAO:
    def __init__(self):
        self.coll = db["unconfirmed_users"]

    # Create
    def insert_one(self, user):
        self.coll.insert_one(user.data)

    # Read
    def find_one(self, query):
        data = self.coll.find_one(query)
        if data:
            return UnconfirmedUser(data, password_hash=True)
        else:
            return None

    def find_one_by_id(self, _id):
        query = {"_id": _id}
        return self.find_one(query)

    def find_one_by_object(self, user):
        query = {"_id": user.id}
        return self.find_one(query)

    def find_one_by_link(self, user):
        query = {"link": user.link}
        return self.find_one(query)

    def find(self, query):
        all_data = self.coll.find(query)
        return [UnconfirmedUser(data, password_hash=True)
                for data
                in all_data]

    def find_all_users(self):
        query = {}
        return self.find(query)

    def does_username_or_email_exist(self, username=None, email=None):
        if not username and not email:
            raise ValueError("At least one of {username, email} must be not "
                             "None")

        query = {}
        if username:
            query["user.username"] = username
        if email:
            query["user.email"] = email
        if self.coll.find_one(query):
            return True
        else:
            return False

    # Update
    def update_one(self, query, update):
        self.coll.update_one(query, update)

    def update_one_by_id(self, _id, update):
        query = {"_id": _id}
        self.coll.update_one(query, update)

    # Delete
    def delete_one(self, query):
        self.coll.delete_one(query)

    def delete_one_by_id(self, _id):
        query = {"_id": _id}
        self.delete_one(query)

    def delete_one_by_link(self, link):
        query = {"link": link}
        self.delete_one(query)

    def pop(self, query):
        user = self.find_one(query)
        if user:
            self.delete_one(query)
        return user

    def pop_by_id(self, _id):
        user = self.find_one_by_id(_id)
        if user:
            self.delete_one_by_id(_id)
        return user

    def pop_by_link(self, link):
        user = self.find_one_by_link(link)
        if user:
            self.delete_one_by_link(link)
        return user

    def confirm_user(self, link=None):
        if not link:
            raise ValueError("No registration link provided")

        query = {"link": link}
        user = self.pop(query)

        if user:
            confirmed_user_data = user.user_data
            confirmed_user = User(confirmed_user_data, password_hash=True)
            confirmed_dao = ConfirmedUserDAO()
            confirmed_dao.insert_one(confirmed_user)
        return user
