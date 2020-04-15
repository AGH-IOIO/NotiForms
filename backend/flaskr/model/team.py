from .utils import parse_id
from ..auth import as_jwt
from flask import url_for
from ..email import send_email


class Team:
    """
    JSON format:
    {
      _id: ObjectId,
      name: string,        # unique
      users: list[string]  # usernames
    }
    """

    def __init__(self, data):
        self.data = data
        self.data["_id"] = parse_id(data)

    @property
    def id(self):
        return self.data["_id"]

    @id.setter
    def id(self, new_id):
        self.data["_id"] = new_id

    @property
    def name(self):
        return self.data["name"]

    @name.setter
    def name(self, new_name):
        self.data["name"] = new_name

    @property
    def users(self):
        return self.data["users"]

    @users.setter
    def users(self, new_users):
        self.data["users"] = new_users

    def add_user(self, username):
        if username not in self.data["users"]:
            self.data["users"].append(username)

    def remove_user(self, username):
        self.data["users"].remove(username)

    def is_user_in_team(self, username):
        return username in self.data["users"]

    def get_invitation_link(self, username):
        token = as_jwt({"username": username,
                        "team_name": self.name})
        return url_for('confirm_team', token=token, _external=True)

    def invite_user(self, user):
        send_email(user.email, 'Confirm team invitation', 'invitation_email',
                   username=user.username, link=self.get_invitation_link(user.username),
                   team_name=self.name)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.data)
