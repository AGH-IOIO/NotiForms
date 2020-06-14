from . import get_with_auth, flask_client, clear_db, stub_user, stub_template_form

from ..model.message_box import Message
from ..database.message_box_dao import MessageBoxDAO

from datetime import datetime, timedelta


def test_get_user_messages(clear_db, flask_client, stub_user, stub_template_form):
    current_time = datetime.utcnow()
    username = stub_user["username"]
    _, _, form = stub_template_form

    message_data = {
        "text": "AAAA",
        "send_date": current_time,
        "ref_id": form.id
    }
    message = Message(message_data)

    message_box_dao = MessageBoxDAO()
    message_box_dao.add_message(message, owner=username)

    res = get_with_auth(flask_client, "/messages/{}/".format(username))
    assert res.status_code == 200

    res_json = res.get_json()
    assert "messages" in res_json

    messages_list = res_json["messages"]
    assert len(messages_list) > 0

    filtered_list = list(filter(lambda x: x["text"] == message_data["text"], messages_list))
    assert len(filtered_list) > 0
