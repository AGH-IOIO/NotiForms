from datetime import datetime

from bson import ObjectId

from .utils import parse_id


class FormResults:
    # results of sent forms, created from a template
    """
    JSON format:
    {
      _id: ObjectId,
      owner: string,  # username
      title: string,
      send_date: date,
      deadline: date,
      finished: bool,
      not_filled_yet: list[string],  # usernames
      questions: list[
                   {
                     type: string,  # one of the available question types
                     title: string,
                   }
                 ],
      answers: list[
                 {
                   username: string,
                   answers: list[varies]  # appropriate for the question type
                 }
               ],
      notification_details: list[
                 {
                   type: string,
                   dead_period: int,
                   before_deadline_frequency: int,
                   after_deadline_frequency: int
                 }
               ],
    }
    """

    def __init__(self, data, form_title=None, recipients=None, deadline=None, notification_details=None, from_db=False):
        if from_db:
            self._data = data
            self._data["_id"] = parse_id(data)
            return

        if not recipients:
            raise ValueError("You must provide recipients when creating "
                             "FormResults from a template (and not from db)")

        self._data = dict()
        self._data["_id"] = ObjectId()
        self._data["owner"] = data.owner
        self._data["title"] = form_title
        self._data["send_date"] = datetime.utcnow()
        self._data["deadline"] = deadline
        self._data["finished"] = datetime.utcnow() > deadline if deadline else False
        self._data["not_filled_yet"] = recipients
        self._data["questions"] = [{"type": question.type,
                                    "title": question.title}
                                   for question in data.questions]
        self._data["answers"] = []
        self._data["notification_details"] = None

        if notification_details:
            self._data["notification_details"] = [{
                "type": notification_detail.type,
                "dead_period": notification_detail.dead_period,
                "before_deadline_frequency": notification_detail.before_deadline_frequency,
                "after_deadline_frequency": notification_detail.after_deadline_frequency}
                for notification_detail in notification_details
            ]

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
    def finished(self):
        return self._data["finished"]

    @finished.setter
    def finished(self, new_finished):
        self._data["finished"] = new_finished

    def mark_as_finished(self):
        self._data["finished"] = True

    def check_if_finished_and_set(self):
        self._data["finished"] = datetime.utcnow() < self._data["deadline"] if self._data["deadline"] else False

    @property
    def not_filled_yet(self):
        return self._data["not_filled_yet"]

    @not_filled_yet.setter
    def not_filled_yet(self, new_not_filled_yet):
        self._data["not_filled_yet"] = new_not_filled_yet

    def users_that_filled(self):
        return [answer["username"] for answer in self._data["answers"]]

    @property
    def questions(self):
        return self._data["questions"]

    @questions.setter
    def questions(self, new_questions):
        self._data["questions"] = new_questions

    @property
    def answers(self):
        return self._data["answers"]

    @answers.setter
    def answers(self, new_answers):
        self._data["answers"] = new_answers

    def add_answers_from_form(self, form):
        username = form.recipient
        answers = [question["answer"] for question in form.questions]
        self._data["not_filled_yet"].remove(username)
        self._data["answers"] = {"username": username,
                                 "answers": answers}

    @property
    def notification_details(self):
        return self._data["notification_details"]

    @notification_details.setter
    def notification_details(self, new_details):
        self._data["notification_details"] = new_details

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self._data)
