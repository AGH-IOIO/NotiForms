from . import db
from ..model.forms import Template


class TemplateDAO:
    def __init__(self):
        self.coll = db["templates"]

    # Create
    def insert_one(self, template):
        self.coll.insert_one(template.data)

    # Read
    def find_one(self, query):
        data = self.coll.find_one(query)
        if data:
            return Template(data)
        else:
            return None

    def find_one_by_id(self, _id):
        query = {"_id": _id}
        return self.find_one(query)

    def find_one_by_object(self, template):
        query = {"_id": template.id}
        return self.find_one(query)

    def find(self, query):
        all_data = self.coll.find(query)
        return [Template(data)
                for data
                in all_data]

    def find_all_for_owner(self, owner_username):
        query = {"owner": owner_username}
        return self.find(query)

    # Update
    def update_one(self, query, update):
        self.coll.update_one(query, update)

    def update_one_by_id(self, _id, update):
        query = {"_id": _id}
        self.coll.update_one(query, update)

    def update_one_by_name(self, team_name, update):
        query = {"name": team_name}
        self.coll.update_one(query, update)

    # Delete
    def delete_one(self, query):
        self.coll.delete_one(query)

    def delete_one_by_id(self, _id):
        query = {"_id": _id}
        self.coll.delete_one(query)
