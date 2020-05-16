from datetime import datetime, timedelta
from bson.json_util import dumps
import pytest

from . import post_with_auth, flask_client, stub_user, clear_db
from ..database import db
from ..database.templates_dao import TemplateDAO
from ..database.form_results_dao import FormResultsDAO
from ..database.pending_forms_dao import PendingFormsDAO
from ..model.forms import Template, Form
from ..model.results import FormResults


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

    results = FormResults(template, recipients=["stubUser"], deadline=deadline)
    results_dao = FormResultsDAO()
    results_dao.insert_one(results)

    form_data = {
        "recipient": "stubUser",
        "results_id": results.id,
        "form": template.data
    }
    form = Form(form_data)
    forms_dao = PendingFormsDAO()
    forms_dao.insert_one(form)

    return template, results, form


def test_fill_form(clear_db, flask_client, stub_user, stub_template_form):
    _, results, form = stub_template_form
    user = stub_user

    answers = [1, "aaaa", [0, 2]]
    post_data = {
        "form_id": form.id,
        "answers": answers,
        "recipient": user["username"]
    }

    # dumps used to be able to JSON serialize ObjectID
    res = post_with_auth(flask_client, "/forms/fill/", dumps(post_data))
    assert res.status_code == 200

    results_dao = FormResultsDAO()
    results = results_dao.find_one_by_id(results.id)

    assert user["username"] not in results.not_filled_yet

    users_with_answers = list(map(lambda x: x["username"], results.answers))
    assert user["username"] in users_with_answers

    forms_dao = PendingFormsDAO()
    form = forms_dao.find_one_by_id(form.id)
    assert form is None
