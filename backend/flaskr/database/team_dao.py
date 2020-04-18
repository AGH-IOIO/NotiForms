from . import db
from ..model.team import Team


class TeamDAO:
    def __init__(self):
        self.coll = db["teams"]

    # Create
    def insert_one(self, team):
        self.coll.insert_one(team.data)

    # Read
    def find_one(self, query):
        data = self.coll.find_one(query)
        if data:
            return Team(data)
        else:
            return None

    def find_one_by_id(self, _id):
        query = {"_id": _id}
        return self.find_one(query)

    def find_one_by_object(self, team):
        query = {"_id": team.id}
        return self.find_one(query)

    def find_one_by_name(self, team_name):
        query = {"name": team_name}
        return self.find_one(query)

    def find(self, query):
        all_data = self.coll.find(query)
        return [Team(data)
                for data
                in all_data]

    def find_all_teams(self):
        query = {}
        return self.find(query)

    def does_team_name_exist(self, team_name):
        query = {"name": team_name}
        if self.coll.find_one(query):
            return True
        else:
            return False

    def is_user_in_team(self, username, team_name=None, _id=None):
        if not team_name and not _id:
            raise ValueError("At least one of {team_name, _id} must be not "
                             "None")

        query = {}
        if team_name:
            query["name"] = team_name
        if _id:
            query["_id"] = _id

        query["users"] = username

        if self.coll.find_one(query):
            return True
        else:
            return False

    def is_name_available(self, team_name):
        query = {"name": team_name}
        if self.coll.find_one(query):
            return False
        else:
            return True

    def find_users_from_team(self, team_name=None, _id=None):
        if not team_name and not _id:
            raise ValueError("At least one of {team_name, _id} must be not "
                             "None")

        query = {}
        if team_name:
            query["name"] = team_name
        if _id:
            query["_id"] = _id

        team = self.find_one(query)
        if team:
            return team.members
        else:
            return None

    # Update
    def update_one(self, query, update):
        self.coll.update_one(query, update)

    def update_one_by_id(self, _id, update):
        query = {"_id": _id}
        self.coll.update_one(query, update)

    def update_one_by_name(self, team_name, update):
        query = {"name": team_name}
        self.coll.update_one(query, update)

    def change_name(self, new_team_name, old_team_name=None, _id=None):
        if not old_team_name and not _id:
            raise ValueError("At least one of {old_team_name, _id} must be "
                             "not None")

        query = {}
        if old_team_name:
            query["name"] = old_team_name
        if _id:
            query["_id"] = _id

        update = {"$set": {"name": new_team_name}}
        self.coll.update_one(query, update)

    def add_user(self, username, team_name=None, _id=None):
        if not team_name and not _id:
            raise ValueError("At least one of {team_name, _id} must be not "
                             "None")

        query = {}
        if team_name:
            query["name"] = team_name
        if _id:
            query["_id"] = _id

        update = {"$push": {"users": username}}
        self.coll.find_one_and_update(query, update)

    def remove_user(self, username, team_name=None, _id=None):
        if not team_name and not _id:
            raise ValueError("At least one of {team_name, _id} must be not "
                             "None")

        query = {}
        if team_name:
            query["name"] = team_name
        if _id:
            query["_id"] = _id

        update = {"$pull": {"users": username}}
        self.coll.find_one_and_update(query, update)

    # Delete
    def delete_one(self, query):
        self.coll.delete_one(query)

    def delete_one_by_id(self, _id):
        query = {"_id": _id}
        self.coll.delete_one(query)

    def delete_one_by_name(self, team_name):
        query = {"name": team_name}
        self.coll.delete_one(query)
