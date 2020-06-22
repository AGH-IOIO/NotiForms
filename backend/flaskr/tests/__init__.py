import json
import os
from datetime import datetime, timedelta

import pytest

from ..auth import as_jwt
from ..database import connection
from ..database.form_results_dao import FormResultsDAO
from ..database.message_box_dao import MessageBoxDAO
from ..database.pending_forms_dao import PendingFormsDAO
from ..database.templates_dao import TemplateDAO
from ..database.user_dao import UserDAO
from ..model.forms import Template, Form
from ..model.message_box import MessageBox
from ..model.results import FormResults
from ..model.user import User
from ...flaskr import app


@pytest.fixture
def flask_client():
    # This gives better error messages.
    app.config["TESTING"] = True

    # Return flask client
    with app.test_client() as client:
        yield client


@pytest.fixture
def clear_db():
    # clear the entire database
    connection.drop_database(os.environ["DB_NAME"])


@pytest.fixture
def stub_user():
    data = {
        "username": "stubUser",
        "password": "123456789",
        "email": "stubmail@gmail.com"
    }
    new_user = User(dict(data))
    dao = UserDAO()
    dao.insert_one(new_user)

    message_box = MessageBox({
        "owner": data["username"],
        "messages": []
    })
    message_box_dao = MessageBoxDAO()
    message_box_dao.insert_one(message_box)

    return data


@pytest.fixture
def stub_template_form():
    question1 = {
        "type": "single_choice",
        "title": "Czy jesteś na nie?",
        "choices": ["TAK", "NIE"],
        "answer": -1
    }
    question2 = {
        "type": "open_text",
        "title": "Napisz coś o sobie?",
        "answer": ""
    }
    question3 = {
        "type": "multiple_choice",
        "title": "Czy?",
        "choices": ["TAK", "NIE", "NIE WIEM"],
        "answer": []
    }

    template_data = {
        "owner": "team_owner",
        "title": "Referendum",
        "questions": [question1, question2, question3]
    }
    template = Template(template_data)
    template_dao = TemplateDAO()
    template_dao.insert_one(template)

    send_date = datetime.utcnow()
    deadline = send_date + timedelta(days=1.0)

    form_title = "AAAAA"
    results = FormResults(template, form_title=form_title, recipients=["stubUser"])
    results_dao = FormResultsDAO()
    results_dao.insert_one(results)

    form_data = {
        "title": form_title,
        "recipient": "stubUser",
        "results_id": results.id,
        "template": template.data,
        "deadline": deadline
    }
    form = Form(form_data)
    PendingFormsDAO().insert_one(form)

    return template, results, form


def auth_token(username):
    return as_jwt({"username": username})


def get(client, path, headers=None):
    if headers is None:
        headers = {}
    return client.get(path, headers=headers)


def get_with_auth(client, path, username="pietrek"):
    headers = {
        "Authorization": auth_token(path)
    }
    return get(client, path, headers=headers)


def post(client, path, data={}, headers={}):
    return client.post(
        path,
        data=json.dumps(data),
        content_type="application/json",
        headers=headers
    )


def post_with_auth(client, path, data, username="pietrek"):
    # TODO: Add user with that username into DB.
    headers = {
        "Authorization": auth_token(path)
    }
    return post(client, path, data, headers)
