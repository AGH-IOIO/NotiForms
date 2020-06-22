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
      title: string,
      send_date: date,
      deadline: date,
      last_notify: data,     # date of last notification
      notify_period: int,    # number of seconds to wait before sending next periodic notification(after exceeding deadline)
      results_id: ObjectId,  # FormResults id
      template: Template  # with filled answer fields in questions
    }
    """

    def __init__(self, data):
        data["_id"] = parse_id(data)
        if "send_date" not in data:
            data["send_date"] = datetime.utcnow()
        self._data = data

    @property
    def data(self):
        new_data = dict()
        new_data["_id"] = self.id
        new_data["title"] = self.title
        new_data["recipient"] = self.recipient
        new_data["send_date"] = self.send_date
        new_data["deadline"] = self.deadline
        new_data["results_id"] = self.results_id
        new_data["template"] = self.template
        new_data["last_notify"] = self.last_notify
        new_data["notify_period"] = self.last_notify
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
    def title(self):
        return self._data["title"]

    @title.setter
    def title(self, new_title):
        self._data["title"] = new_title

    @property
    def send_date(self):
        return self._data["send_date"]

    @send_date.setter
    def send_date(self, new_send_date):
        self._data["send_date"] = new_send_date

    @property
    def deadline(self):
        return self._data["deadline"]

    @deadline.setter
    def deadline(self, new_deadline):
        self._data["deadline"] = new_deadline

    @property
    def last_notify(self):
        return self._data.get("last_notify")

    @last_notify.setter
    def last_notify(self, new_last_notify):
        self._data["last_notify"] = new_last_notify

    @property
    def notify_period(self):
        return self._data.get("notify_period", 60)

    @notify_period.setter
    def notify_period(self, new_notify_period):
        self._data["notify_period"] = new_notify_period

    @property
    def results_id(self):
        return self._data["results_id"]

    @results_id.setter
    def results_id(self, new_results_id):
        self._data["results_id"] = new_results_id

    @property
    def template(self):
        return self._data["template"]

    @template.setter
    def template(self, new_template):
        self._data["template"] = new_template

    @property
    def questions(self):
        return self.template["questions"]

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self._data)
