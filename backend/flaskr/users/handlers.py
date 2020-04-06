from flask import g, jsonify

from flaskr import app
from flaskr.validate import Validator, mk_error, expect_mime, json_body
from flaskr.auth import as_jwt, auth_required

from .model import UserD

import re


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

    # Token should be issued only after successful check.
    # Check if user exists
    username = body["username"]
    user = UserD.get_user({"username": username})
    if user is None:
        return mk_error("There is no user with this name")

    # Check password
    if not user.verify_password(body["password"]):
        return mk_error("Incorrect password")

    # Issue a token
    token_data = {"username": username}
    token = as_jwt(token_data)
    return jsonify({"token": token})


@app.route("/users/", methods=["GET"])
@auth_required
def list_users():
    users = [user.as_dict() for user in UserD.list_users({})]
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

    email_format = lambda x: re.match(r'[A-Za-z][A-Za-z0-9_\.]*@[A-Za-z0-9_]+\.[A-Za-z0-9_]', x)
    validator.field_predicate(
        "email", email_format,
        mk_error("Incorrect email format")
    )

    # If there was an error, send response
    error_res = validator.error()
    if error_res is not None:
        return error_res

    new_user = UserD.create_user(body["username"], body["email"], body["password"])
    if new_user is None:
        return mk_error("User with given name or email already exists.")

    return jsonify(new_user.as_dict())
