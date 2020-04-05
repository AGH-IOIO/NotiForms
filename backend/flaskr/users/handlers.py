from flask import request, jsonify, Response

from flaskr import app
from flaskr.db import db
from flaskr.validate import Validator, mk_error

from .model import UserD


@app.route("/users/", methods=["POST"])
def mk_user():
    validator = Validator(request)

    validator.field_present("username")
    validator.field_present("email")
    validator.field_present("password")
    validator.field_predicate(
        "password",
        lambda x: len(str(x)) >= 5,
        mk_error("Password must be at least 5 characters long")
    )

    error_res = validator.error()
    if error_res is not None:
        return error_res

    body = request.json

    new_user = UserD()
    new_user.username = body["username"]
    new_user.email = body["email"]
    new_user.password = body["password"]

    return jsonify(new_user.as_dict())
