from bson import ObjectId
from flask import Blueprint, g, jsonify

from .. import app
from ..auth import auth_required
from ..database.form_results_dao import FormResultsDAO
from ..database.message_box_dao import MessageBoxDAO
from ..database.pending_forms_dao import PendingFormsDAO
from ..database.user_dao import UserDAO
from ..model.utils import check_answer_type
from ..validate import expect_mime, json_body, Validator, mk_error

form_bp = Blueprint("forms", __name__)


def validate_form_body(body):
    validator = Validator(body)
    validator.field_present("form_id")
    validator.field_present("answers")
    validator.field_present("recipient")
    return validator.error()


def insert_answers_to_db(body):
    form_id = ObjectId(body["form_id"])
    recipient = body["recipient"]

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
    results_dao.add_answers_from_user(answers, recipient, results_id)
    forms_dao.delete_one_by_id(form_id)

    message_box_dao = MessageBoxDAO()
    message_box_dao.remove_message(form_id, recipient)


@app.route("/forms/fill/", methods=["POST"])
@expect_mime("application/json")
@json_body
@auth_required
def fill_form():
    # json.loads needed to correctly deserialize ObjectId
    body = g.body
    error_res = validate_form_body(body)

    if error_res is not None:
        return mk_error("Invalid data")

    result = insert_answers_to_db(body)
    if result is not None:  # check if there was an error
        return result

    return jsonify({"confirmation": "OK"})


@app.route("/forms/pending/<username>/", methods=["GET"])
@auth_required
def get_user_pending_forms(username):
    """
    Returns pending forms of currently logged in user.
    """
    user = UserDAO().find_one_by_username(username)
    if user is None:
        return mk_error("Invalid username")

    forms = PendingFormsDAO().find_all_for_user(username)
    forms_dict = [form.data for form in forms]
    return jsonify({"forms": forms_dict})


@app.route("/forms/results/<results_id>/", methods=["GET"])
@auth_required
def get_form_results(results_id):
    """
    Returns results of a given form
    """
    results_dao = FormResultsDAO()

    results = results_dao.find_one_by_id(ObjectId(results_id))
    if results is None:
        return mk_error("Invalid results_id")

    return jsonify({"results": results.data})


@app.route("/forms/owned/<username>/", methods=["GET"])
@auth_required
def get_forms_owned_by_user(username):
    """
    Returns list of results objects owned by given user - in fact it is a list of forms made by this user
    """
    results_dao = FormResultsDAO()

    results_list = results_dao.find_all_for_owner(username)
    if results_list is None:
        return mk_error("User does not exist or does not own any forms yet")

    results_data = [result.data for result in results_list]
    return jsonify({"forms": results_data})
