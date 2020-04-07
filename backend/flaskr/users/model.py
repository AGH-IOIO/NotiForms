from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.db import db

class UserD(object):
    def __init__(self):
        self._username = None
        self._email = None
        self._password = None

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new_username):
        self._username = new_username

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        self._email = new_email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        self._password = generate_password_hash(new_password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)

    def as_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "username": self.username
        }

    @staticmethod
    def list_users(query):
        return [UserD.from_dict(user) for user in db["users"].find(query)]

    @staticmethod
    def get_user(query):
        user_dict = db["users"].find_one(query)
        if user_dict is None:
            return None

        return UserD.from_dict(db["users"].find_one(query))

    @staticmethod
    def create_user(username, email, password):
        user = UserD.get_user({"$or": [{"username": username}, {"email": email}]})
        if user is not None:
            return None

        user = UserD()
        user.username = username
        user.email = email
        user.password = password
        db["users"].insert_one(user.as_dict())

        return user

    @staticmethod
    def from_dict(d):
        user = UserD()
        user.username = d.get("username", None)
        user.email = d.get("email", None)
        user.password = d.get("password", "")
        return user

