from bson import ObjectId
from flask import url_for

from ..auth import as_jwt, mk_error
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


def check_answer_type(question_type, answer):
    if question_type == "open_text":
        if isinstance(answer, str):
            return True
    elif question_type == "single_choice":
        if isinstance(answer, int):
            return True
    elif question_type == "multiple_choice":
        if isinstance(answer, list):
            for element in answer:
                if not isinstance(element, int):
                    return False
            return True

    return False


def create_user_registration_link(username):
    token = as_jwt({"username": username})
    return url_for('confirm', token=token, _external=True)


def create_team_invitation_for_user_link(team_name, username):
    token = as_jwt({"username": username,
                    "team_name": team_name})
    return url_for('confirm_team', token=token, _external=True)


def invite_user_to_team(team_name, username):
    from ..database.user_dao import UserDAO

    dao = UserDAO()
    user = dao.find_one({"username": username})

    if user is not None:
        send_email(user.email,
                   'Confirm team invitation',
                   'invitation_email',
                   username=user.username,
                   link=create_team_invitation_for_user_link(team_name, user.username),
                   team_name=team_name)
    return user


def confirm_user(link=None):
    from ..database.unconfirmed_user_dao import UnconfirmedUserDAO
    from ..database.message_box_dao import MessageBoxDAO
    from ..database.user_dao import UserDAO
    from ..model.user import User
    from ..model.message_box import MessageBox

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

        message_box = MessageBox({
            "owner": user.username,
            "messages": []
        })
        message_box_dao = MessageBoxDAO()
        message_box_dao.insert_one(message_box)
    return user


def add_user_to_team(username, team_name):
    from ..database.user_dao import UserDAO
    from ..database.team_dao import TeamDAO

    team_dao = TeamDAO()
    user_dao = UserDAO()

    if not user_dao.does_username_or_email_exist(username=username):
        return mk_error("User with given name does not exist")

    team_dao.add_user(username, team_name=team_name)
    user_dao.add_team(team_name, username=username)
    return None


def save_new_team(body, invited_members):
    from ..database.team_dao import TeamDAO
    from ..database.user_dao import UserDAO
    from ..model.team import Team

    team_data = {
        "name": body["name"],
        "members": [body["owner"]],
        "invited": invited_members
    }
    team = Team(team_data)
    team_dao = TeamDAO()
    user_dao = UserDAO()

    if team_dao.does_team_name_exist(team.name):
        return mk_error("Team with this name already exists!")
    else:
        team_dao.insert_one(team)
        user_dao.add_team(team.name, body["owner"])
        return None
