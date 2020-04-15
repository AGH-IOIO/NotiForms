from abc import ABC, abstractmethod

from .utils import *


class Question(ABC):
    """
    Abstract parent class of all concrete question types, defined in utils.py.
    """

    @abstractmethod
    def __init__(self, data):
        data["_id"] = parse_id(data)
        check_question_type(data["type"])
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
    def type(self):
        return self._data["type"]

    @type.setter
    def type(self, new_type):
        self._data["type"] = new_type

    @property
    def title(self):
        return self._data["title"]

    @title.setter
    def title(self, new_title):
        self._data["title"] = new_title

    @property
    def answer(self):
        return self._data["answer"]

    @answer.setter
    def answer(self, new_answer):
        self._data["answer"] = new_answer

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self._data)


class OpenTextQuestion(Question):
    """
    JSON format:
    {
      _id: ObjectId,
      type: string,  # must be "open_text"
      title: string,
      answer: string  # default: "" (before answering, default in creation)
    }
    """

    def __init__(self, data):
        super().__init__(data)
        if self.type != "open_text":
            error_msg = "Tried to assign question of type {} to a " + \
                        "OpenTextQuestion!".format(self.type)
            raise ValueError(error_msg)

        if "answer" not in data:
            self._data["answer"] = ""


class SingleChoiceQuestion(Question):
    """
    JSON format:
    {
      _id: ObjectId,
      type: string,  # must be "single_choice"
      title: string,
      choices: list[string],
      answer: int  # index of chosen choice, default: -1 (before answering)
    }
    """

    def __init__(self, data):
        super().__init__(data)
        if self.type != "open_text":
            error_msg = "Tried to assign question of type {} to a " + \
                        "SingleChoiceQuestion!".format(self.type)
            raise ValueError(error_msg)

        if "answer" not in data:
            self._data["answer"] = -1

    @property
    def choices(self):
        return self._data["choices"]

    @choices.setter
    def choices(self, new_choices):
        self._data["choices"] = new_choices

    def add_choice(self, new_choice, index=None):
        if index:
            self._data["choices"].insert(index, new_choice)
        else:
            self._data["choices"].append(new_choice)

    def remove_choice(self, new_choice, index=None):
        if index:
            del self._data["choices"][index]
        else:
            self._data["choices"].remove(new_choice)


class MultipleChoiceQuestion(Question):
    """
    JSON format:
    {
      _id: ObjectId,
      type: string,  # must be "single_choice"
      title: string,
      choices: list[string],
      answer: list[int]  # indices of chosen choices, default: []
    }
    """

    def __init__(self, data):
        super().__init__(data)
        if self.type != "open_text":
            error_msg = "Tried to assign question of type {} to a " + \
                        "MultipleChoiceQuestion!".format(self.type)
            raise ValueError(error_msg)

        if "answer" not in data:
            self._data["answer"] = []

    @property
    def choices(self):
        return self._data["choices"]

    @choices.setter
    def choices(self, new_choices):
        self._data["choices"] = new_choices

    def add_choice(self, new_choice=None, index=None):
        if index:
            self._data["choices"].insert(index, new_choice)
        else:
            self._data["choices"].append(new_choice)

    def remove_choice(self, choice=None, index=None):
        if choice:
            self._data["choices"].remove(choice)
        elif index:
            del self._data["choices"][index]
        else:
            raise ValueError("At least one of {choice, index} must be not "
                             "None")

    def add_answer(self, new_answer):
        self._data["answer"].append(new_answer)

    def remove_answer(self, answer=None, index=None):
        if answer:
            self._data["answer"].remove(answer)
        elif index:
            del self._data["answer"][index]
        else:
            raise ValueError("At least one of {answer, index} must be not "
                             "None")


class MultipleChoiceQuestion(Question):
    """
    JSON format:
    {
      _id: ObjectId,
      type: string,  # must be "single_choice"
      title: string,
      choices: list[string],
      answer: list[int]  # indices of chosen choices, default: []
    }
    """

    def __init__(self, data):
        super().__init__(data)
        if self.type != "open_text":
            error_msg = "Tried to assign question of type {} to a " + \
                        "MultipleChoiceQuestion!".format(self.type)
            raise ValueError(error_msg)

        if "answer" not in data:
            self._data["answer"] = []

    @property
    def choices(self):
        return self._data["choices"]

    @choices.setter
    def choices(self, new_choices):
        self._data["choices"] = new_choices

    def add_choice(self, new_choice=None, index=None):
        if index:
            self._data["choices"].insert(index, new_choice)
        else:
            self._data["choices"].append(new_choice)

    def remove_choice(self, choice=None, index=None):
        if choice:
            self._data["choices"].remove(choice)
        elif index:
            del self._data["choices"][index]
        else:
            raise ValueError("At least one of {choice, index} must be not "
                             "None")

    def add_answer(self, new_answer):
        self._data["answer"].append(new_answer)

    def remove_answer(self, answer=None, index=None):
        if answer:
            self._data["answer"].remove(answer)
        elif index:
            del self._data["answer"][index]
        else:
            raise ValueError("At least one of {answer, index} must be not "
                             "None")
