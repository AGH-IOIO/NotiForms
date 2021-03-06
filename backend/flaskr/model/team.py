from .utils import parse_id


class Team:
    """
    JSON format:
    {
      _id: ObjectId,
      name: string,        # unique
      members: list[string]  # usernames
      invited: list[string]  # usernames of uncofirmed members
    }
    """

    def __init__(self, data):
        data["_id"] = parse_id(data)
        self._data = data

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
    def name(self):
        return self._data["name"]

    @name.setter
    def name(self, new_name):
        self._data["name"] = new_name

    @property
    def members(self):
        return self._data["members"]

    @members.setter
    def members(self, new_members):
        self._data["members"] = new_members

    @property
    def invited(self):
        return self._data["invited"]

    @invited.setter
    def invited(self, new_invited):
        self._data["invited"] = new_invited

    def add_user(self, username):
        if username not in self._data["members"]:
            self._data["members"].append(username)

        if username in self._data["invited"]:
            self._data["invited"].remove(username)

    def remove_user(self, username):
        self._data["members"].remove(username)

    def is_user_in_team(self, username):
        return username in self._data["members"]

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self._data)
