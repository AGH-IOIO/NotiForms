from werkzeug.security import generate_password_hash, check_password_hash
from .utils import parse_id


class User(object):
    def __init__(self, data, password_hash=False):
        data["_id"] = parse_id(data)
        self.data = data
        if not password_hash:
            self.data["password"] = generate_password_hash(data["password"])

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

    @property
    def teams(self):
        return self.data["teams"]

    @teams.setter
    def teams(self, new_teams):
        self.data["teams"] = new_teams

    def add_team(self, team_name):
        if team_name not in self.data["teams"]:
            self.data["teams"].append(team_name)

    def remove_team(self, team_name):
        try:
            self.data["teams"].remove(team_name)
        except ValueError:
            pass

    def change_team(self, old_team_name, new_team_name):
        try:
            index = self.data["teams"].index(old_team_name)
            self.data["teams"][index] = new_team_name
        except ValueError:
            pass

    def is_user_in_team(self, team_name):
        return team_name in self.data["teams"]

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.data)
