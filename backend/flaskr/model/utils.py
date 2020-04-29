from bson import ObjectId
from flask import url_for

from .questions import *
from ..email import send_email
from ..auth import as_jwt


def parse_id(data):
    if "_id" not in data:
        return ObjectId()
    _id = data["_id"]
    if isinstance(_id, str):
        return ObjectId(_id)
    elif isinstance(_id, ObjectId):
        return _id
    else:
        raise ValueError("_id has to be of string or ObjectId type")


def check_question_type(question_type):
    allowed_types = {"open_text", "single_choice", "multiple_choice",
                     "date"}
    if question_type not in allowed_types:
        error_msg = "Question type \"" + question_type + "\" is not supported"
        raise ValueError(error_msg)


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


def create_user_registration_link(username):
    token = as_jwt({"username": username})
    return url_for('confirm', token=token, _external=True)


def create_team_invitation_for_user_link(team, username):
    token = as_jwt({"username": username,
                    "team_name": team.name})
    return url_for('confirm_team', token=token, _external=True)


def invite_user_to_team(team, user):
    send_email(user.email,
               'Confirm team invitation',
               'invitation_email',
               username=user.username,
               link=create_team_invitation_for_user_link(team, user.username),
               team_name=team.name)
