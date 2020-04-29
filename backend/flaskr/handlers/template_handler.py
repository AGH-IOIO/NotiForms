from flask import jsonify, Blueprint, g

from .. import app
from ..auth import auth_required
from ..database.templates_dao import TemplateDAO
from ..model.form import Template
from ..validate import expect_mime, json_body, Validator, mk_error

template_bp = Blueprint('templates', __name__)


def validate_template(body):
    validator = Validator(body)
    validator.field_present("owner")
    validator.field_present("title")
    validator.field_present("questions")
    return validator.error()


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
