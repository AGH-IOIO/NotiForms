from . import db
from ..model.message_box import MessageBox


class MessageBoxDAO:
    def __init__(self):
        self.coll = db["message_boxes"]

    # Create
    def insert_one(self, msg_box):
        self.coll.insert_one(msg_box.data)

    # Read
    def find_one(self, query):
        data = self.coll.find_one(query)
        if data:
            return MessageBox(data)
        else:
            return None

    def find_one_by_id(self, _id):
        query = {"_id": _id}
        return self.find_one(query)

    def find_one_by_object(self, team):
        query = {"_id": team.id}
        return self.find_one(query)

    def find(self, query):
        all_data = self.coll.find(query)
        return [MessageBox(data)
                for data
                in all_data]

    def find_all_for_user(self, owner):
        query = {"owner": owner}
        return self.find(query)

    # Update
    def update_one(self, query, update):
        self.coll.update_one(query, update)

    def update_one_by_id(self, _id, update):
        query = {"_id": _id}
        self.coll.update_one(query, update)

    def update_one_by_owner(self, owner, update):
        query = {"owner": owner}
        self.coll.update_one(query, update)

    def add_message(self, msg, owner=None, _id=None):
        if not owner and not _id:
            raise ValueError("At least one of {owner, _id} must be not "
                             "None")

        query = {}
        if owner:
            query["owner"] = owner
        if _id:
            query["_id"] = _id

        update = {"$push": {"messages": msg.data}}
        self.coll.find_one_and_update(query, update)

    def remove_message(self, msg_ref_id, owner=None, _id=None):
        if not owner and not _id:
            raise ValueError("At least one of {owner, _id} must be not "
                             "None")

        query = {}
        if owner:
            query["owner"] = owner
        if _id:
            query["_id"] = _id

        update = {"$pull": {"messages": {"ref_id": msg_ref_id}}}
        self.coll.find_one_and_update(query, update)

    # Delete
    def delete_one(self, query):
        self.coll.delete_one(query)

    def delete_one_by_id(self, _id):
        query = {"_id": _id}
        self.coll.delete_one(query)
