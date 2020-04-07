from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


def create_user_from_dict(data):
    if not data:
        return None

    user = User()
    user.username = data.get("username", None)
    user.email = data.get("email", None)
    user.password = data.get("password", "")
    return user


class User(object):
    def __init__(self, _id=None, username=None, email=None, password=None):
        if self._check_if_exists(username, email):
            raise ValueError("User exists")

        self._id = _id if _id else ObjectId()
        self._username = username
        self._email = email
        self._password = password

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
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "username": self.username
        }

    def _check_if_exists(self, username, email):
        from database.user_dao import UserDAO
        dao = UserDAO()
        query = {"$or": []}
        if username:
            query["$or"].append({"username": username})
        if email:
            query["$or"].append({"email": email})
        if dao.find_one(query) is not None:
            return True
        else:
            return False
