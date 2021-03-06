from datetime import datetime

from flask import jsonify, Blueprint, g

from .. import app
from ..auth import auth_required
from ..database.form_results_dao import FormResultsDAO
from ..database.message_box_dao import MessageBoxDAO
from ..database.pending_forms_dao import PendingFormsDAO
from ..database.team_dao import TeamDAO
from ..database.templates_dao import TemplateDAO
from ..model.forms import Template, Form
from ..model.message_box import Message
from ..model.results import FormResults
from ..validate import expect_mime, json_body, Validator, mk_error

template_bp = Blueprint('templates', __name__)


def validate_template(body):
    validator = Validator(body)
    validator.field_present("owner")
    validator.field_present("title")
    validator.field_present("questions")
    return validator.error()


def send_forms_to_db(body):
    team_dao = TeamDAO()
    if not team_dao.is_user_in_team(body["owner"], team_name=body["team"]):
        return mk_error("Given template owner is not a member of a team with given name")

    team_members = team_dao.find_users_from_team(team_name=body["team"])
    if team_members is None:
        return mk_error("Team with given name does not exist")
    team_members = list(filter(lambda x: x != body["owner"], team_members))

    template_dao = TemplateDAO()
    template = template_dao.find_one({
        "owner": body["owner"],
        "title": body["template_title"]
    })
    if not template:
        return mk_error("Template with given owner and title does not exist")

    form_title = body["title"]
    try:
        results = FormResults(template, form_title=form_title, recipients=team_members)
    except ValueError:
        return mk_error("Error with creating form results object, team members list is empty (maybe you are trying to "
                        "send form only to yourself?)")

    results_dao = FormResultsDAO()
    results_dao.insert_one(results)
    results_id = results.id

    send_date = datetime.utcnow()
    deadline = datetime.strptime(body["deadline"], "%Y-%m-%d %H:%M")
    notification_details = body["notification_details"]
    for details in notification_details:
        details["notify_date"] = send_date

    print("Inserting " + str(deadline), flush=True)

    pending_forms_dao = PendingFormsDAO()
    message_box_dao = MessageBoxDAO()

    forms_to_insert = []

    for member in team_members:
        try:
            form = Form({
                "title": form_title,
                "template": template.data,
                "deadline": deadline,
                "send_date": send_date,
                "notification_details": notification_details
            })
        except ValueError:
            return mk_error("Invalid type of notification given")

        form.recipient = member
        form.results_id = results_id

        forms_to_insert.append(form)
        form_id = form.id
        message = Message({
            "text": "New form to fill",
            "send_date": send_date,
            "ref_id": form_id
        })
        message_box_dao.add_message(message, owner=member)

    pending_forms_dao.insert_many(forms_to_insert)
    return None


@app.route("/templates/create/", methods=["POST"])
@expect_mime("application/json")
@json_body
@auth_required
def create_template():
    body = g.body
    error_res = validate_template(body)
    if error_res is not None:
        return mk_error("Invalid data")

    try:
        template = Template(body)
    except ValueError:
        return mk_error("Invalid question types")

    dao = TemplateDAO()
    dao.insert_one(template)
    return jsonify({"confirmation": "OK"})


@app.route("/templates/assign/", methods=["POST"])
@expect_mime("application/json")
@json_body
@auth_required
def assign_template_to_team():
    body = g.body
    validator = Validator(body)
    validator.field_present("title")
    validator.field_present("team")
    validator.field_present("owner")
    validator.field_present("template_title")
    validator.field_present("deadline")
    error_res = validator.error()
    if error_res is not None:
        return mk_error("Invalid data")

    result = send_forms_to_db(body)
    if result is not None:
        return result

    return jsonify({"confirmation": "OK"})


@app.route("/templates/get_templates/<username>/", methods=["GET"])
@auth_required
def get_user_templates(username):
    template_dao = TemplateDAO()
    user_templates = template_dao.find_all_for_owner(username)

    return jsonify({"templates": [x.data for x in user_templates]})
