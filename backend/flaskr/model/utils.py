from bson import ObjectId
from flask import url_for

from ..auth import as_jwt
from ..email import send_email


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


def confirm_user(link=None):
    from ..database.unconfirmed_user_dao import UnconfirmedUserDAO
    from ..database.user_dao import UserDAO
    from ..model.user import User

    if not link:
        raise ValueError("No registration link provided")

    unconfirmed_dao = UnconfirmedUserDAO()
    query = {"link": link}
    user = unconfirmed_dao.pop(query)

    if user:
        confirmed_user_data = user.user_data
        confirmed_user = User(confirmed_user_data, password_hash=True)
        confirmed_dao = UserDAO()
        confirmed_dao.insert_one(confirmed_user)
    return user
