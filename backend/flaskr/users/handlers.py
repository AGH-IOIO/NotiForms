from flask import request, Response

from flaskr import app
from flaskr.db import db

from .model import UserD

@app.route("/users/", methods=['GET'])
def users():
    res = Response(str(db))
    res.headers["Content-Type"] = "text/plain"
    return res

@app.route("/users/", methods=["POST"])
def mk_user():
    new_user = UserD()
    new_user.username = request.form.get("username", None)
    new_user.email = request.form.get("email", None)
    db.append(new_user)

    res = Response(str(new_user))
    res.headers["Content-Type"] = "text/plain"
    return res

@app.route("/users/<int:user_id>", methods=["GET", "PUT"])
def user(user_id):
    res = Response()
    res.headers["Content-Type"] = "text/plain"
    res.data = str(db[user_id]) if user_id >= 0 and user_id < len(db) else "Invalid user"
    return res
