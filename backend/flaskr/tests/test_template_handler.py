from datetime import datetime, timedelta
import pytest

from . import post_with_auth, flask_client, stub_user, clear_db
from ..database import db
from ..database.user_dao import UserDAO
from ..database.message_box_dao import MessageBoxDAO
from ..database.templates_dao import TemplateDAO
from ..database.pending_forms_dao import PendingFormsDAO
from ..database.team_dao import TeamDAO
from ..model.user import User
from ..model.team import Team
from ..model.forms import Template
from ..model.message_box import MessageBox


@pytest.fixture
def stub_user():
    user_data = {
        "username": "new_user",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }
    dao = UserDAO()
    user = User(user_data)
    dao.insert_one(user)

    return user


def test_create_template(clear_db, flask_client, stub_user):
    question1 = {
        "type": "single_choice",
        "title": "Single choice?",
        "choices": ["No", "Yes"]
    }
    question2 = {
        "type": "multiple_choice",
        "title": "Multiple choice",
        "choices": ["One", "two", "four"]
    }
    question3 = {
        "type": "open_text",
        "title": "Open text question",
    }
    template = {
        "owner": stub_user.username,
        "title": "Test template",
        "questions": [question1, question2, question3]
    }

    res = post_with_auth(flask_client, "/templates/create/", template)
    assert res.status_code == 200

    dao = TemplateDAO()
    template_from_db = dao.find_one({
        "owner": template["owner"],
        "title": template["title"]
    })

    assert template_from_db is not None
    questions = template_from_db.questions
    titles = list(map(lambda x: x.title, questions))

    assert question1["title"] in titles
    assert question2["title"] in titles
    assert question3["title"] in titles


def test_assign_template_to_team(clear_db, flask_client, stub_user):
    message_box_dao = MessageBoxDAO()
    message_box = MessageBox({
        "owner": stub_user.username,
        "messages": []
    })
    message_box_dao.insert_one(message_box)

    owner_data = {
        "username": "team_owner",
        "password": "123456789",
        "email": "stubmail@gmail.tm"
    }
    user_dao = UserDAO()
    owner = User(owner_data)
    user_dao.insert_one(owner)

    question = {
        "type": "single_choice",
        "title": "Single choice?",
        "choices": ["Of course", "Yes"]
    }
    template_data = {
        "owner": "team_owner",
        "title": "Test template",
        "questions": [question]
    }
    team_data = {
        "name": "stub_team",
        "members": ["new_user", "team_owner"]
    }
    team = Team(team_data)
    team_dao = TeamDAO()
    team_dao.insert_one(team)

    template_dao = TemplateDAO()
    template = Template(template_data)
    template_dao.insert_one(template)

    post_data = {
        "team": "stub_team",
        "owner": "team_owner",
        "template_title": template.title,
        "deadline": (datetime.utcnow() + timedelta(days=1.0)).strftime("%Y-%m-%d %H:%M:%S.%f")
    }

    res = post_with_auth(flask_client, "/templates/assign/", post_data)
    assert res.status_code == 200

    message_box = message_box_dao.find_all_for_user(stub_user.username)
    message = message_box[0].messages[0]

    assert message["text"] == "New form to fill"

    pending_forms_dao = PendingFormsDAO()
    pending_form = pending_forms_dao.find_all_for_user(stub_user.username)[0]

    assert message["ref_id"] == pending_form.id
