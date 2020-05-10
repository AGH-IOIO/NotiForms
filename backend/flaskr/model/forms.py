from bson import ObjectId
from datetime import datetime

from .questions import parse_questions
from .utils import parse_id


class Template:
    # form base, from which forms for sending will be created
    """
    JSON format:
    {
      _id: ObjectId,
      owner: string,  # username
      title: string,
      questions: list[Question]  # list of Question documents
    }
    """

    def __init__(self, data):
        print(data)
        data["_id"] = parse_id(data)
        data["questions"] = parse_questions(data["questions"])
        self._data = data

    @property
    def data(self):
        new_data = dict()
        new_data["_id"] = self.id
        new_data["owner"] = self.owner
        new_data["title"] = self.title
        new_data["questions"] = []
        for question in self.questions:
            new_data["questions"].append(question.data)
        return new_data

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
    def owner(self):
        return self._data["owner"]

    @owner.setter
    def owner(self, new_owner):
        self._data["owner"] = new_owner

    @property
    def title(self):
        return self._data["title"]

    @title.setter
    def title(self, new_title):
        self._data["title"] = new_title

    @property
    def questions(self):
        return self._data["questions"]

    @questions.setter
    def questions(self, new_questions):
        self._data["questions"] = new_questions

    def add_question(self, question, index=None):
        if index:
            self._data["questions"].insert(index, question)
        else:
            self._data["questions"].append(question)

    def remove_question(self, question=None, index=None):
        if index:
            del self._data["questions"][index]
        elif question:
            self._data["questions"].remove(question)
        else:
            raise ValueError("At least one of {question, index} must be not "
                             "None")

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self._data)


class Form:
    # active form, created from template, sent and not yet filled
    """
    JSON format:
    {
      _id: ObjectId,
      recipient: string,  # username
      send_date: date,
      results_id: ObjectId,  # FormResults id
      form: Template  # with filled answer fields in questions
    }
    """

    def __init__(self, data):
        data["_id"] = parse_id(data)
        if "send_date" not in data:
            data["send_date"] = datetime.utcnow()
        #data["form"] = Template(data["form"]).data
        self._data = data

    @property
    def data(self):
        new_data = dict()
        new_data["_id"] = self.id
        new_data["recipient"] = self.recipient
        new_data["send_date"] = self.send_date
        new_data["results_id"] = self.results_id
        new_data["form"] = self.form
        return new_data

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
    def recipient(self):
        return self._data["recipient"]

    @recipient.setter
    def recipient(self, new_recipient):
        self._data["recipient"] = new_recipient

    @property
    def send_date(self):
        return self._data["send_date"]

    @send_date.setter
    def send_date(self, new_send_date):
        self._data["send_date"] = new_send_date

    @property
    def results_id(self):
        return self._data["results_id"]

    @results_id.setter
    def results_id(self, new_results_id):
        self._data["results_id"] = new_results_id

    @property
    def form(self):
        return self._data["form"]

    @form.setter
    def form(self, new_form):
        self._data["form"] = new_form

    @property
    def questions(self):
        return self.form.questions

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self._data)
