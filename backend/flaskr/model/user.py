from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


class User(object):
    def __init__(self, data, password_hash=False):
        self.data = data
        self._parse_id()
        if not password_hash:
            self.data["password"] = generate_password_hash(data["password"])

    def _parse_id(self):
        if "_id" not in self.data:
            self.data["_id"] = ObjectId()
        _id = self.data["_id"]
        if isinstance(_id, str):
            self.data["_id"] = ObjectId(_id)
        elif isinstance(_id, ObjectId):
            return
        else:
            raise ValueError("_id has to be of string or ObjectId type")

    @property
    def _id(self):
        return self.data["_id"]

    @_id.setter
    def _id(self, new_id):
        self.data["_id"] = new_id

    @property
    def username(self):
        return self.data["username"]

    @username.setter
    def username(self, new_username):
        self.data["username"] = new_username

    @property
    def email(self):
        return self.data["email"]

    @email.setter
    def email(self, new_email):
        self.data["email"] = new_email

    @property
    def password(self):
        return self.data["password"]

    @password.setter
    def password(self, new_password):
        self.data["password"] = generate_password_hash(new_password)

    def set_hashed_password(self, password):
        """
        This method sets the password directly, without hashing it before. It
        should be used ONLY when the password argument is a hash.
        :param password: hashed password
        """
        self.data["password"] = password

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.data)
