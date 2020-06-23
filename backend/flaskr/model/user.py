from werkzeug.security import generate_password_hash, check_password_hash

from .utils import parse_id


class User:
    """
    JSON format:
    {
      _id: ObjectId,
      username: string,    # unique
      email: string,       # unique
      password: string,     # hash, not plaintext
      teams: list[string],  # team names
      push_subscription_info: list[{
            user_agent: string,
            subscription_info: dict
        }
    }
    """

    def __init__(self, data, password_hash=False):
        data["_id"] = parse_id(data)

        if "push_subscription_info" not in data:
            data["push_subscription_info"] = []
        self._data = data
        if not password_hash:
            self._data["password"] = generate_password_hash(data["password"])

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
    def username(self):
        return self._data["username"]

    @username.setter
    def username(self, new_username):
        self._data["username"] = new_username

    @property
    def email(self):
        return self._data["email"]

    @email.setter
    def email(self, new_email):
        self._data["email"] = new_email

    @property
    def password(self):
        return self._data["password"]

    @password.setter
    def password(self, new_password):
        self._data["password"] = generate_password_hash(new_password)

    def set_hashed_password(self, password):
        """
        This method sets the password directly, without hashing it before. It
        should be used ONLY when the password argument is a hash.
        :param password: hashed password
        """
        self._data["password"] = password

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def teams(self):
        return self._data["teams"]

    @teams.setter
    def teams(self, new_teams):
        self._data["teams"] = new_teams

    @property
    def push_subscription_info(self):
        return self._data["push_subscription_info"]

    @push_subscription_info.setter
    def push_subscription_info(self, new_info):
        self._data["push_subscription_info"] = new_info

    def add_team(self, team_name):
        if team_name not in self._data["teams"]:
            self._data["teams"].append(team_name)

    def remove_team(self, team_name):
        try:
            self._data["teams"].remove(team_name)
        except ValueError:
            pass

    def change_team(self, old_team_name, new_team_name):
        try:
            index = self._data["teams"].index(old_team_name)
            self._data["teams"][index] = new_team_name
        except ValueError:
            pass

    def is_user_in_team(self, team_name):
        return team_name in self._data["teams"]

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self._data)
