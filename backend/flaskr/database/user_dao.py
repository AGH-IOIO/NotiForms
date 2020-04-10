from . import db
from ..model.user import create_user_from_dict


class UserDAO:
    def __init__(self):
        self.coll = db["users"]

    # Create
    def insert_one(self, user):
        self.coll.insert_one(user.as_dict())

    # Read
    def find_one(self, query, as_json=False):
        user_data = self.coll.find_one(query)
        if as_json:
            return user_data
        else:
            return create_user_from_dict(user_data, password_hash=True)

    def find_one_by_id(self, _id, as_json=False):
        query = {"_id": _id}
        return self.find_one(query, as_json=as_json)

    def find_one_by_user_object(self, user, as_json=False):
        query = {"_id": user._id}
        return self.find_one(query, as_json=as_json)

    def find(self, query, as_json=False):
        users_data = self.coll.find(query)
        if as_json:
            return list(users_data)
        else:
            return [create_user_from_dict(data, password_hash=True)
                    for data
                    in users_data]

    def find_all_users(self, as_json=False):
        query = {}
        return self.find(query, as_json=as_json)

    def does_username_or_email_exist(self, username=None, email=None):
        query = {"$or": []}
        if username:
            query["$or"].append({"username": username})
        if email:
            query["$or"].append({"email": email})
        if self.find_one(query) is not None:
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
