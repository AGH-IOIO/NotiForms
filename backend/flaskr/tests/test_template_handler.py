from datetime import datetime, timedelta
import pytest

from . import post_with_auth, get_with_auth, flask_client, stub_user, clear_db
from ..database import db
from ..database.user_dao import UserDAO
from ..database.form_results_dao import FormResultsDAO
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
        "title": "test_form",
        "team": "stub_team",
        "owner": "team_owner",
        "template_title": template.title,
        "deadline": (datetime.utcnow() + timedelta(days=1.0)).strftime("%Y-%m-%d %H:%M"),
        "notification_details": [
            {
                "type": "push",
                "dead_period": 72000,
                "before_deadline_frequency": 18000,
                "after_deadline_frequency": 9000
            },
            {
                "type": "e-mail",
                "dead_period": 36000,
                "before_deadline_frequency": 9000,
                "after_deadline_frequency": 4500
            }
        ]
    }

    res = post_with_auth(flask_client, "/templates/assign/", post_data)
    assert res.status_code == 200

    message_box = message_box_dao.find_for_user(stub_user.username)
    message = message_box.messages[0]

    assert message["text"] == "New form to fill"

    pending_forms_dao = PendingFormsDAO()
    pending_form = pending_forms_dao.find_all_for_user(stub_user.username)[0]

    assert message["ref_id"] == pending_form.id

    form_results_dao = FormResultsDAO()
    results = form_results_dao.find_one({"title": post_data["title"],
                                         "owner": post_data["owner"]})
    assert results is not None
    assert len(results.notification_details) == len(post_data["notification_details"])

    notification_details = results.notification_details
    assert any(x["type"] == "push" for x in notification_details)
    assert any(x["type"] == "e-mail" for x in notification_details)
    assert any(x["dead_period"] == 36000 for x in notification_details)


def test_get_user_templates(clear_db, flask_client, stub_user):
    question1 = {
        "type": "single_choice",
        "title": "Single choice1?",
        "choices": ["Of course", "Yes"]
    }
    question2 = {
        "type": "single_choice",
        "title": "Single choice2?",
        "choices": ["Of course", "Yes"]
    }
    question3 = {
        "type": "single_choice",
        "title": "Single choice3?",
        "choices": ["Of course", "Yes"]
    }

    template1_data = {
        "owner": stub_user.username,
        "title": "My template1",
        "questions": [question1, question2]
    }

    template2_data = {
        "owner": stub_user.username,
        "title": "My template2",
        "questions": [question3]
    }

    template1 = Template(template1_data)
    template2 = Template(template2_data)
    template_dao = TemplateDAO()
    template_dao.insert_one(template1)
    template_dao.insert_one(template2)

    res = get_with_auth(flask_client, "/templates/get_templates/" + stub_user.username + "/")
    assert res.status_code == 200

    templates = res.get_json()["templates"]
    titles = list(map(lambda x: x["title"], templates))

    assert template1.title in titles
    assert template2.title in titles


def test_get_user_templates_with_no_templates(clear_db, flask_client, stub_user):
    res = get_with_auth(flask_client, "/templates/get_templates/" + stub_user.username + "/")
    assert res.status_code == 200

    templates = res.get_json()["templates"]
    assert len(templates) == 0
