from flask import request, jsonify

from flaskr import app
from flaskr.db import db
from flaskr.validate import Validator, mk_error
from flaskr.auth import as_jwt, from_jwt

from .model import UserD

@app.route("/token/", methods=["POST"])
def make_token():
    validator = Validator(request)
    body = request.json

    validator.field_present("username")
    validator.field_present("password")
    error_res = validator.error()
    if error_res is not None:
        return error_res

    # TODO: Use 'username' to get user from db
    #       then perform password check.
    # Token should be issued only after successful check.

    # Issue a token
    token_data = {"username": body["username"]}
    token = as_jwt(token_data)
    return jsonify({"token": token})

@app.route("/users/", methods=["GET"])
def list_users():
    # TODO: DAO should provide method for querying users collection.
    users = [UserD.from_dict(user).as_dict() for user in db["users"].find()]
    return jsonify({"users": users})

@app.route("/users/", methods=["POST"])
def make_user():
    validator = Validator(request)
    body = request.json

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

    new_user = UserD()
    new_user.username = body["username"]
    new_user.email = body["email"]
    new_user.password = body["password"]

    # TODO: DAO should provide methods for creating new entries.
    db["users"].insert_one(new_user.as_dict())
    return jsonify(new_user.as_dict())
