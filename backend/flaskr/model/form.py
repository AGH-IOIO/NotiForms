from .questions import *


def parse_questions(questions):
    result = []
    type_to_class = {"open_text": OpenTextQuestion,
                     "single_choice": SingleChoiceQuestion,
                     "multiple_choice": MultipleChoiceQuestion}
                     #"single_date": SingleDateQuestion,
                     #"multiple_date": MultipleDateQuestion}

    for question in questions:
        q_type = question.type
        if q_type not in type_to_class:
            raise ValueError("Question type {} not recognized".format(q_type))
        else:
            question_class = type_to_class[q_type]
            question_object = question_class(question)
            result.append(question_object)

    return result


class Template:
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
        self._data = data
        data["questions"] = parse_questions(self._data["questions"])

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
