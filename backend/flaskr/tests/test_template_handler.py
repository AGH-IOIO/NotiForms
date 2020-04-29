import pytest

from . import post_with_auth, flask_client, stub_user, clear_db
from ..database import db
from ..database.user_dao import UserDAO
from ..database.templates_dao import TemplateDAO
from ..model.user import User


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
