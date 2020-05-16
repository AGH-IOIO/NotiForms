import json

from bson import ObjectId
from flask import Blueprint, g, jsonify

from .. import app
from ..auth import auth_required
from ..database.form_results_dao import FormResultsDAO
from ..database.pending_forms_dao import PendingFormsDAO
from ..model.utils import check_answer_type
from ..validate import expect_mime, json_body, Validator, mk_error

form_bp = Blueprint("forms", __name__)


def validate_form_body(body):
    validator = Validator(body)
    validator.field_present("form_id")
    validator.field_present("answers")
    validator.field_present("recipient")
    return validator.error()


@app.route("/forms/fill/", methods=["POST"])
@expect_mime("application/json")
@json_body
@auth_required
def fill_form():
    # json.loads needed to correctly deserialize ObjectId
    body = json.loads(g.body)
    error_res = validate_form_body(body)

    if error_res is not None:
        return mk_error("Invalid data")

    form_id = ObjectId(body["form_id"]["$oid"])
    forms_dao = PendingFormsDAO()
    form = forms_dao.find_one_by_id(form_id)
    if form is None:
        return mk_error("Form with given id does not exist")

    answers = body["answers"]
    if len(form.questions) != len(answers):
        return mk_error("Number of given answers does not match with number of questions in form")

    for question, answer in zip(form.questions, answers):
        if not check_answer_type(question["type"], answer):
            return mk_error("Invalid answer for question: {}".format(question["title"]))

    results_id = form.results_id
    results_dao = FormResultsDAO()

    results_dao.add_answers_from_user(answers, body["recipient"], results_id)

    forms_dao.delete_one_by_id(form_id)
    return jsonify({"confirmation": "OK"})
