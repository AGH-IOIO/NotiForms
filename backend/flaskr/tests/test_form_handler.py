from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId
import pytest

from . import post_with_auth, get_with_auth, flask_client, stub_user, clear_db
from ..database import db
from ..database.message_box_dao import MessageBoxDAO
from ..database.templates_dao import TemplateDAO
from ..database.form_results_dao import FormResultsDAO
from ..database.pending_forms_dao import PendingFormsDAO
from ..model.forms import Template, Form
from ..model.results import FormResults
from ..model.message_box import MessageBox


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
        "title": "AAAAA",
        "recipient": "stubUser",
        "results_id": results.id,
        "form": template.data
    }
    form = Form(form_data)
    PendingFormsDAO().insert_one(form)

    return template, results, form


def test_fill_form(clear_db, flask_client, stub_user, stub_template_form):
    _, results, form = stub_template_form
    user = stub_user

    answers = [1, "aaaa", [0, 2]]
    post_data = {
        "form_id": str(form.id),
        "answers": answers,
        "recipient": user["username"]
    }

    message_box_dao = MessageBoxDAO()
    message_box_data = {
        "owner": user["username"],
        "messages": [{
            "text": "AAAAAAAAAAAAAAAA",
            "send_date": datetime.utcnow(),
            "ref_id": form.id
        }]
    }
    message_box = MessageBox(message_box_data)
    message_box_dao.insert_one(message_box)

    # dumps used to be able to JSON serialize ObjectID
    res = post_with_auth(flask_client, "/forms/fill/", post_data)
    assert res.status_code == 200

    results_dao = FormResultsDAO()
    results = results_dao.find_one_by_id(results.id)

    assert user["username"] not in results.not_filled_yet

    users_with_answers = list(map(lambda x: x["username"], results.answers))
    assert user["username"] in users_with_answers

    messages = message_box_dao.find_all_for_user(user["username"])[0].messages
    filtered_messages = list(filter(lambda x: x["ref_id"] == form.id, messages))
    assert len(filtered_messages) == 0

    forms_dao = PendingFormsDAO()
    form = forms_dao.find_one_by_id(form.id)
    assert form is None


def test_get_pending_forms(clear_db, flask_client, stub_user, stub_template_form):
    _, results, form = stub_template_form
    user = stub_user

    # Try invalid user
    res = get_with_auth(flask_client, "/forms/pending/wereżniesz/")
    assert res.status_code == 400

    # Try valid user with one pending
    res = get_with_auth(flask_client, "/forms/pending/%s/" % user["username"])
    assert res.status_code == 200
    res_json = res.get_json()
    assert "forms" in res_json
    res_forms = res_json["forms"]
    assert len(res_forms) == 1
    res_form = res_forms[0]

    # IMO ObjectId shouldn't be exposed outside model classes.
    # Aftern sending ObjectId from controller it becomes String.
    # That's way I have to use nasty tricks such as:
    l = PendingFormsDAO().find_one_by_id(ObjectId(res_form["_id"])).data
    r = form.data
    # Side effects in Form constructor fuck everyting up
    del l["send_date"]
    del r["send_date"]
    assert l == r

    # Fillup form
    post_data = {
        "form_id": str(form.id),
        "answers": [1, "aaaa", [0, 2]],
        "recipient": user["username"]
    }
    res = post_with_auth(flask_client, "/forms/fill/", post_data)
    assert res.status_code == 200

    # Make sure it's not longer in pending
    res = get_with_auth(flask_client, "/forms/pending/%s/" % user["username"])
    assert res.status_code == 200
    res_json = res.get_json()
    assert "forms" in res_json
    res_forms = res_json["forms"]
    assert len(res_forms) == 0


def test_get_form_results(clear_db, flask_client, stub_user, stub_template_form):
    _, results, form = stub_template_form
    user = stub_user

    results_dao = FormResultsDAO()
    answers = [0, "AAA", [0, 2]]
    results_dao.add_answers_from_user(answers, user["username"], results.id)

    res = get_with_auth(flask_client, "/forms/results/{}/".format(str(results.id)))
    assert res.status_code == 200

    res_json = res.get_json()
    results = res_json["results"]
    assert len(results["not_filled_yet"]) == 0
    assert len(results["answers"]) == 1

    res_answers = results["answers"][0]
    assert res_answers["username"] == user["username"]
    assert res_answers["answers"] == answers
