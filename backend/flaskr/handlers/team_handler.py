import os

from flask import jsonify, Blueprint, g

from .. import app
from ..auth import from_jwt, auth_required
from ..database.team_dao import TeamDAO
from ..model.team import Team
from ..validate import expect_mime, json_body, Validator, mk_error

team_bp = Blueprint('teams', __name__)


@app.route("/teams/confirm_team/<token>")
def confirm_team(token):
    token_data = from_jwt(token)
    dao = TeamDAO()

    username = token_data["username"]
    team_name = token_data["team_name"]

    if dao.is_user_in_team(username, team_name=team_name):
        return jsonify({"confirmation": "Already confirmed"})
    else:
        dao.add_user(username, team_name=team_name)
        return jsonify({"confirmation": "OK"})
    # TODO - redirect somewhere


def validate_team_body(body):
    validator = Validator(body)
    validator.field_present("name")
    validator.field_present("members")
    return validator.error()


@app.route("/teams/create_team_fast/", methods=["POST"])
@expect_mime("application/json")
@json_body
def create_fast_team_with_users():
    body = g.body
    error_res = validate_team_body(body)

    if error_res is not None:
        return error_res

    team_data = {
        "name": body["name"],
        "members": body["members"]
    }

    team = Team(team_data)
    dao = TeamDAO()
    if dao.does_team_name_exist(team.name):
        return mk_error("Team with this name already exists!")

    dao.insert_one(team)

    return jsonify({"confirmation": "OK"})


@app.route("/teams/create_team/", methods=["POST"])
@expect_mime("application/json")
@json_body
def create_team():
    body = g.body
    error_res = validate_team_body(body)

    if error_res is not None:
        return error_res

    team_data = {
        "name": body["name"],
        "members": []
    }
    invited_members = body["members"]

    team = Team(team_data)
    dao = TeamDAO()
    if dao.does_team_name_exist(team.name):
        return mk_error("Team with this name already exists!")

    dao.insert_one(team)

    from ..model.utils import invite_user_to_team
    for invited_member_name in invited_members:
        if os.environ["TEST"] != 'y':
            if invite_user_to_team(team, invited_member_name) is None:
                return mk_error("User " + invited_member_name + " does not exist!")

    return jsonify({"confirmation": "OK"})


@app.route("/teams/get_members/<team_name>")
@auth_required
def get_team_members(team_name):
    dao = TeamDAO()
    if not dao.does_team_name_exist(team_name):
        return mk_error("Team with given name does not exist!")

    members = dao.find_users_from_team(team_name)
    return jsonify({"members": members})
