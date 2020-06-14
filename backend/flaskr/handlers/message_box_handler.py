from flask import Blueprint, jsonify

from .. import app
from ..auth import auth_required
from ..database.message_box_dao import MessageBoxDAO

message_box_bp = Blueprint("messages", __name__)


@app.route("/messages/<username>/", methods=["GET"])
@auth_required
def get_user_messages(username):
    message_box_dao = MessageBoxDAO()
    user_messages = message_box_dao.find_all_for_user(username)

    return jsonify({"messages": sum([message.data["messages"] for message in user_messages], [])})
