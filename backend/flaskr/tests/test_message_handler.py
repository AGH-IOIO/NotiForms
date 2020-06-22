from . import get_with_auth, post_with_auth, flask_client, clear_db, stub_user, stub_template_form

from ..model.message_box import Message
from ..database.message_box_dao import MessageBoxDAO

from datetime import datetime


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


def test_mark_messages_as_viewed(clear_db, flask_client, stub_user, stub_template_form):
    current_time = datetime.utcnow()
    username = stub_user["username"]
    _, _, form = stub_template_form

    message_box_dao = MessageBoxDAO()
    messages = []
    for i in range(0, 3):
        message = Message({
            "text": i * "AAA",
            "send_date": current_time,
            "ref_id": form.id
        })
        messages.append(message)
        assert not message.viewed
        message_box_dao.add_message(message, owner=username)

    post_data = {
        "owner": username,
        "ids": [str(messages[0].id), str(messages[2].id)]
    }
    res = post_with_auth(flask_client, "/messages/mark_as_viewed/", post_data)
    assert res.status_code == 200

    message_box = message_box_dao.find_for_user(username)
    read_messages = message_box.messages
    assert len(read_messages) == len(messages)

    unviewed_messages = list(filter(lambda x: not x["viewed"], read_messages))
    assert len(unviewed_messages) == 1
    assert any(message["_id"] == messages[1].id for message in unviewed_messages)

    viewed_messages = list(filter(lambda x: x["viewed"], read_messages))
    assert len(viewed_messages) == 2
    assert any(message["_id"] == messages[0].id for message in viewed_messages)
    assert any(message["_id"] == messages[2].id for message in viewed_messages)
