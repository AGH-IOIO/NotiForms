from werkzeug.security import generate_password_hash, check_password_hash

from .user import User
from .utils import parse_id


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
        user = User(new_data["user"])
        new_data["user"] = user.data
        self.data = new_data

    @property
    def id(self):
        return self.data["_id"]

    @id.setter
    def id(self, new_id):
        self.data["_id"] = new_id

    @property
    def link(self):
        return self.data["link"]

    @link.setter
    def link(self, new_link):
        self.data["link"] = new_link

    @property
    def username(self):
        return self.data["user"]["username"]

    @username.setter
    def username(self, new_username):
        self.data["user"]["username"] = new_username

    @property
    def email(self):
        return self.data["user"]["email"]

    @email.setter
    def email(self, new_email):
        self.data["user"]["email"] = new_email

    @property
    def password(self):
        return self.data["user"]["password"]

    @password.setter
    def password(self, new_password):
        self.data["user"]["password"] = generate_password_hash(new_password)

    def set_hashed_password(self, password):
        """
        This method sets the password directly, without hashing it before. It
        should be used ONLY when the password argument is a hash.
        :param password: hashed password
        """
        self.data["password"] = password

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def teams(self):
        return self.data["teams"]

    @teams.setter
    def teams(self, new_teams):
        self.data["teams"] = new_teams

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.data)
