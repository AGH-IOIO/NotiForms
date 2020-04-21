import pytest

from . import get_with_auth, post, post_with_auth, flask_client, \
    stub_user, clear_db, get, app
from ..database import db
from ..database.user_dao import UserDAO
from ..database.team_dao import TeamDAO
from ..model.user import User
from ..model.team import Team
from ..model.utils import create_team_invitation_for_user_link


def test_confirm_invitation(clear_db, flask_client):
    team_data = {
        "name": "test_team",
        "users": []
    }
    team = Team(team_data)

    user_data = {
        "username": "new_user",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }
    user = User(user_data)

    user_dao = UserDAO()
    team_dao = TeamDAO()

    user_dao.insert_one(user)
    team_dao.insert_one(team)

    with app.test_client(), app.test_request_context():
        invitation_link = create_team_invitation_for_user_link(team, user.username)

    token = invitation_link.split('/')[-1]
    res = get(flask_client, "/teams/confirm_team/" + token)
    assert res.status_code == 200
    assert res.get_json()["confirmation"] == "OK"

    team_from_db = team_dao.find_one_by_name(team.name)
    assert user.username in team_from_db.members
