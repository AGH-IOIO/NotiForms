from .utils import parse_id


class Team(object):
    def __init__(self, data):
        self.data["_id"] = parse_id(data)
        self.data = data

        # TODO: add unique invite link creation and handling

    @property
    def _id(self):
        return self.data["_id"]

    @_id.setter
    def _id(self, new_id):
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

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.data)
