from . import post_with_auth, get_with_auth, flask_client, stub_user, clear_db

from ..database.user_dao import UserDAO


def test_get_public_key(flask_client):
    res = get_with_auth(flask_client, "/push/get_public_key/")
    assert res.status_code == 200

    res_json = res.get_json()
    assert "public_key" in res_json
    assert res_json["public_key"] is not None


def test_subscribe_user(clear_db, flask_client, stub_user):
    username = stub_user["username"]
    post_data = {
        "username": username,
        "user_agent": "internet_explorer",
        "subscription_info": {
            "some": "stuff",
            "aaaa": "bottom_text",
            "hello_there": "General Kenobi!"
        }
    }

    res = post_with_auth(flask_client, "/push/subscribe/", post_data)
    assert res.status_code == 200

    res_json = res.get_json()
    assert "confirmation" in res_json
    assert res_json["confirmation"] == "OK"

    user_dao = UserDAO()
    user = user_dao.find_one_by_username(username)

    push_subscription_info = user.push_subscription_info
    assert len(push_subscription_info) > 0
    assert any(info["user_agent"] == post_data["user_agent"] for info in push_subscription_info)
    assert any(info["subscription_info"] == post_data["subscription_info"] for info in push_subscription_info)
