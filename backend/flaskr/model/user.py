from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


def create_user_from_dict(data, password_hash=False):
    if not data:
        return None

    user = User(**data)

    # if password hash instead of plaintext password was provided, change
    # the attribute appropriately
    if password_hash:
        user.set_hashed_password(data["password"])

    return user


def _parse_id(_id):
    if not _id:
        return ObjectId()
    elif isinstance(_id, str):
        return ObjectId(_id)
    elif isinstance(_id, ObjectId):
        return _id
    else:
        raise ValueError("_id has to be of string or ObjectId type")


class User(object):
    def __init__(self, _id=None, username=None, email=None, password=None):
        self._id = _parse_id(_id)
        self._username = username
        self._email = email
        self._password = generate_password_hash(password)

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

    def set_hashed_password(self, password):
        """
        This method sets the password directly, without hashing it before. It
        should be used ONLY when the password argument is a hash.
        :param password: hashed password
        """
        self._password = password

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def as_dict(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "username": self.username
        }

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.as_dict())
