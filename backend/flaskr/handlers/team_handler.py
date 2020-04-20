from flask import jsonify, Blueprint

from .. import app
from ..auth import from_jwt
from ..database.team_dao import TeamDAO

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
