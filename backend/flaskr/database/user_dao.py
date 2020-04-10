from . import db
from ..model.user import User


class UserDAO:
    def __init__(self):
        self.coll = db["users"]

    # Create
    def insert_one(self, user):
        self.coll.insert_one(user.data)

    # Read
    def find_one(self, query):
        user_data = self.coll.find_one(query)
        return User(user_data, password_hash=True)

    def find_one_by_id(self, _id):
        query = {"_id": _id}
        return self.find_one(query)

    def find_one_by_user_object(self, user):
        query = {"_id": user._id}
        return self.find_one(query)

    def find(self, query):
        users_data = self.coll.find(query)
        return [User(data, password_hash=True)
                for data
                in users_data]

    def find_all_users(self):
        query = {}
        return self.find(query)

    def does_username_or_email_exist(self, username=None, email=None):
        query = {"$or": []}
        if username:
            query["$or"].append({"username": username})
        if email:
            query["$or"].append({"email": email})
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
        self.coll.delete_one(query)
