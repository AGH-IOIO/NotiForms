import os

from flask import jsonify, Blueprint, g

from .. import app
from ..auth import from_jwt, auth_required
from ..database.team_dao import TeamDAO
from ..model.utils import add_user_to_team, save_new_team
from ..validate import expect_mime, json_body, Validator, mk_error

team_bp = Blueprint('teams', __name__)


@app.route("/teams/confirm_team/<token>/", methods=["GET"])
def confirm_team(token):
    token_data = from_jwt(token)
    dao = TeamDAO()

    username = token_data["username"]
    team_name = token_data["team_name"]

    if dao.is_user_in_team(username, team_name=team_name):
        return jsonify({"confirmation": "Already confirmed"})
    else:
        error_res = add_user_to_team(username, team_name)
        if error_res is not None:
            return error_res

        return jsonify({"confirmation": "OK"})
    # TODO - redirect somewhere


def validate_team_body(body):
    validator = Validator(body)
    validator.field_present("name")
    validator.field_present("members")
    validator.field_present("owner")
    return validator.error()


@app.route("/teams/create_team_fast/", methods=["POST"])
@expect_mime("application/json")
@json_body
def create_fast_team_with_users():
    body = g.body
    error_res = validate_team_body(body)

    if error_res is not None:
        return error_res

    error_res = save_new_team(body)
    if error_res is not None:
        return error_res

    team_name = body["name"]
    invited_members = body["members"]

    for member_name in invited_members:
        error_res = add_user_to_team(member_name, team_name)
        if error_res is not None:
            return error_res

    return jsonify({"confirmation": "OK"})


@app.route("/teams/create_team/", methods=["POST"])
@expect_mime("application/json")
@json_body
def create_team():
    body = g.body
    error_res = validate_team_body(body)

    if error_res is not None:
        return error_res

    error_res = save_new_team(body)
    if error_res is not None:
        return error_res

    team_name = body["name"]
    invited_members = body["members"]

    from ..model.utils import invite_user_to_team
    for invited_member_name in invited_members:
        if os.environ["TEST"] != 'y':
            if invite_user_to_team(team_name, invited_member_name) is None:
                return mk_error("User " + invited_member_name + " does not exist!")

    return jsonify({"confirmation": "OK"})


@app.route("/teams/get_members/<team_name>/", methods=["GET"])
@auth_required
def get_team_members(team_name):
    dao = TeamDAO()
    if not dao.does_team_name_exist(team_name):
        return mk_error("Team with given name does not exist!")

    members = dao.find_users_from_team(team_name)
    return jsonify({"members": members})
