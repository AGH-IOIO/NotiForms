from . import db
from ..model.forms import Form


class PendingFormsDAO:
    def __init__(self):
        self.coll = db["pending_forms"]

    # Create
    def insert_one(self, form):
        self.coll.insert_one(form.data)

    def insert_many(self, forms):
        self.coll.insert_many([form.data for form in forms])

    # Read
    def find_one(self, query):
        data = self.coll.find_one(query)
        if data:
            return Form(data)
        else:
            return None

    def find_one_by_id(self, _id):
        query = {"_id": _id}
        return self.find_one(query)

    def find_one_by_object(self, form):
        query = {"_id": form.id}
        return self.find_one(query)

    def fine_one_by_title(self, title):
        query = {"title": title}
        return self.find_one(query)

    def find(self, query):
        all_data = self.coll.find(query)
        return [Form(data)
                for data
                in all_data]

    def find_all_for_user(self, recipient):
        query = {"recipient": recipient}
        return self.find(query)

    # Update
    def update_one(self, query, update):
        self.coll.update_one(query, update)

    def update_one_by_id(self, _id, update):
        query = {"_id": _id}
        self.coll.update_one(query, update)

    def update_one_by_recipient(self, recipient, update):
        query = {"recipient": recipient}
        self.coll.update_one(query, update)

    # Delete
    def delete(self, query):
        self.coll.delete_many(query)

    def delete_one(self, query):
        self.coll.delete_one(query)

    def delete_one_by_id(self, _id):
        query = {"_id": _id}
        self.coll.delete_one(query)

    def pop(self, query):
        form = self.find_one(query)
        if form:
            self.delete_one(query)
        return form

    def pop_by_id(self, _id):
        user = self.find_one_by_id(_id)
        if user:
            self.delete_one_by_id(_id)
        return user

    def pop_by_results_id(self, results_id):
        forms = self.find({"results_id": results_id})
        for form in forms:
            self.delete_one_by_id(form.id)
        return forms
