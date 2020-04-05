from flask import g, jsonify

from flaskr import app
from flaskr.db import db
from flaskr.validate import Validator, mk_error, expect_mime, json_body
from flaskr.auth import as_jwt, auth_required

from .model import UserD

@app.route("/token/", methods=["POST"])
@expect_mime("application/json")
@json_body
def make_token():
    body = g.body
    validator = Validator(body)

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
@auth_required
def list_users():
    # TODO: DAO should provide method for querying users collection.
    users = [UserD.from_dict(user).as_dict() for user in db["users"].find()]
    return jsonify({"users": users})

@app.route("/users/", methods=["POST"])
@expect_mime("application/json")
@json_body
def make_user():
    body = g.body
    validator = Validator(body)

    # Check presence
    validator.field_present("username")
    validator.field_present("email")
    validator.field_present("password")

    # Check if long enough
    min_size = lambda n: lambda x: len(str(x)) >= n
    validator.field_predicate(
        "username", min_size(5),
        mk_error("Username must be at least 5 characters long")
    )
    validator.field_predicate(
        "password", min_size(5),
        mk_error("Password must be at least 5 characters long")
    )

    # TODO: Maybe some email format check?

    # If there was an error, send response
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
