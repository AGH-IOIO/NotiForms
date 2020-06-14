from bson import ObjectId
from flask import Blueprint, jsonify, g

from .. import app
from ..auth import auth_required
from ..database.message_box_dao import MessageBoxDAO
from ..validate import expect_mime, json_body, Validator, mk_error

message_box_bp = Blueprint("messages", __name__)


@app.route("/messages/<username>/", methods=["GET"])
@auth_required
def get_user_messages(username):
    message_box_dao = MessageBoxDAO()
    message_box = message_box_dao.find_for_user(username)

    return jsonify({"messages": message_box.messages})


@app.route("/messages/mark_as_viewed/", methods=["POST"])
@expect_mime("application/json")
@json_body
@auth_required
def mark_messages_as_viewed():
    body = g.body
    validator = Validator(body)
    validator.field_present("ids")
    validator.field_present("owner")
    if validator.error() is not None:
        return mk_error("Invalid data")

    owner = body["owner"]
    # crucial, because find operation fails when using strings instead of ObjectIds
    message_ids = [ObjectId(id_string) for id_string in body["ids"]]
    message_box_dao = MessageBoxDAO()
    message_box_dao.mark_all_messages_from_list_as_viewed(message_ids, owner)

    return jsonify({"confirmation": "OK"})
