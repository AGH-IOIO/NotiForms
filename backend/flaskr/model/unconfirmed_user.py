from werkzeug.security import generate_password_hash, check_password_hash

from .user import User
from .utils import parse_id
from ..auth import as_jwt
from flask import url_for


class UnconfirmedUser:
    """
    JSON format:
    {
      _id: ObjectId,
      link: string,  # registration confirmation link, unique
      user: User document
    }
    """

    def __init__(self, data, password_hash=False):
        new_data = dict()
        new_data["_id"] = parse_id(data)
        new_data["link"] = data["link"]
        user = User(data["user"], password_hash=password_hash)
        new_data["user"] = user.data
        self._data = new_data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @property
    def id(self):
        return self._data["_id"]

    @id.setter
    def id(self, new_id):
        self._data["_id"] = new_id

    @property
    def link(self):
        return self._data["link"]

    @link.setter
    def link(self, new_link):
        self._data["link"] = new_link

    @property
    def username(self):
        return self._data["user"]["username"]

    @username.setter
    def username(self, new_username):
        self._data["user"]["username"] = new_username

    @property
    def email(self):
        return self._data["user"]["email"]

    @email.setter
    def email(self, new_email):
        self._data["user"]["email"] = new_email

    @property
    def password(self):
        return self._data["user"]["password"]

    @password.setter
    def password(self, new_password):
        self._data["user"]["password"] = generate_password_hash(new_password)

    @property
    def user_data(self):
        return self._data["user"]

    @user_data.setter
    def user_data(self, new_user_data):
        self._data["user"] = new_user_data

    @property
    def teams(self):
        return self._data["user"]["teams"]

    @teams.setter
    def teams(self, new_teams):
        self._data["user"]["teams"] = new_teams

    def set_hashed_password(self, password):
        """
        This method sets the password directly, without hashing it before. It
        should be used ONLY when the password argument is a hash.
        :param password: hashed password
        """
        self._data["user"]["password"] = password

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self._data)
