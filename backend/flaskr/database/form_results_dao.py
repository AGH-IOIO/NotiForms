from . import db
from ..model.results import FormResults


class FormResultsDAO:
    def __init__(self):
        self.coll = db["form_results"]

    # Create
    def insert_one(self, form):
        self.coll.insert_one(form.data)

    def insert_many(self, forms):
        self.coll.insert_many([form.data for form in forms])

    # Read
    def find_one(self, query):
        data = self.coll.find_one(query)
        if data:
            return FormResults(data, from_db=True)
        else:
            return None

    def find_one_by_id(self, _id):
        query = {"_id": _id}
        return self.find_one(query)

    def find_one_by_object(self, form):
        query = {"_id": form.id}
        return self.find_one(query)

    def find(self, query):
        all_data = self.coll.find(query)
        return [FormResults(data, from_db=True)
                for data
                in all_data]

    def find_all_for_owner(self, owner_username):
        query = {"owner": owner_username}
        return self.find(query)

    def find_who_did_not_fill_form(self, _id):
        query = {"_id": _id}
        projection = {"_id": False, "not_filled_yet": True}
        return self.coll.find(query, projection)

    # Update
    def update_one(self, query, update):
        self.coll.update_one(query, update)

    def update_one_by_id(self, _id, update):
        query = {"_id": _id}
        self.coll.update_one(query, update)

    def add_answers_from_user(self, answers, username, _id):
        query = {"_id": _id}
        target = {"username": username,
                  "answers": answers}
        update = {"$push": {"answers": target},
                  "$pull": {"not_filled_yet": username}}
        self.coll.find_one_and_update(query, update)

    # Delete
    def delete_one(self, query):
        self.coll.delete_one(query)

    def delete_one_by_id(self, _id):
        query = {"_id": _id}
        self.coll.delete_one(query)
