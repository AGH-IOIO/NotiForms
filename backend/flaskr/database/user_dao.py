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
        data = self.coll.find_one(query)
        return User(data, password_hash=True)

    def find_one_by_id(self, _id):
        query = {"_id": _id}
        return self.find_one(query)

    def find_one_by_object(self, user):
        query = {"_id": user._id}
        return self.find_one(query)

    def find(self, query):
        all_data = self.coll.find(query)
        return [User(data, password_hash=True)
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
            query["username"] = username
        if email:
            query["email"] = email
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

    def change_password(self, new_password,
                        username=None, email=None, _id=None):
        """
        This method should be passed password hash, not plaintext password!
        At least one other argument (username, email or _id) must be provided.
        :param new_password: new password hash
        :param username: string
        :param email: string
        :param _id: string or ObjectId
        """
        if not username and not email and not _id:
            raise ValueError("At least one of {username, email, _id} must be "
                             "not None")

        query = {}
        if username:
            query["username"] = username
        if email:
            query["email"] = email
        if _id:
            query["_id"] = _id

        update = {"$set": {"password": new_password}}
        self.coll.update_one(query, update)

    def add_team(self, team_name, username=None, email=None, _id=None):
        if not username and not email and not _id:
            raise ValueError("At least one of {username, email, _id} must be "
                             "not None")

        query = {}
        if username:
            query["username"] = username
        if email:
            query["email"] = email
        if _id:
            query["_id"] = _id

        update = {"$push": {"teams": team_name}}
        self.coll.find_one_and_update(query, update)

    def remove_team(self, team_name, username=None, email=None, _id=None):
        if not username and not email and not _id:
            raise ValueError("At least one of {username, email, _id} must be "
                             "not None")

        query = {}
        if username:
            query["username"] = username
        if email:
            query["email"] = email
        if _id:
            query["_id"] = _id

        update = {"$pull": {"teams": team_name}}
        self.coll.find_one_and_update(query, update)

    # Delete
    def delete_one(self, query):
        self.coll.delete_one(query)

    def delete_one_by_id(self, _id):
        query = {"_id": _id}
        self.coll.delete_one(query)
