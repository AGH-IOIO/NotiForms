import os

from flask import Blueprint, jsonify, g

from .. import app
from ..auth import auth_required
from ..database.user_dao import UserDAO
from ..validate import mk_error, expect_mime, json_body, Validator

push_bp = Blueprint("push", __name__)


@app.route("/push/get_public_key/", methods=["GET"])
@auth_required
def get_public_key():
    result = os.getenv("PUBLIC_KEY")
    if result is not None:
        return jsonify({"public_key": result})
    else:
        return mk_error("Public key is not set on server")


@app.route("/push/subscribe/", methods=["POST"])
@expect_mime("application/json")
@json_body
@auth_required
def subscribe_user():
    body = g.body
    if validate_subscription_data(body) is not None:
        return mk_error("Invalid data")

    save_subscription_info_to_db(body)

    return jsonify({"confirmation": "OK"})


def validate_subscription_data(body):
    validator = Validator(body)
    validator.field_present("username")
    validator.field_present("user_agent")
    validator.field_present("subscription_info")
    return validator.error()


def save_subscription_info_to_db(body):
    username = body["username"]
    user_agent = body["user_agent"]
    subscription_info = body["subscription_info"]

    user_dao = UserDAO()
    user_dao.save_push_subscription_info(username, user_agent, subscription_info)
