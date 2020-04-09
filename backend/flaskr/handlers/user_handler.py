from flask import g, jsonify, Blueprint

from .. import app
from ..validate import Validator, mk_error, expect_mime, json_body
from ..auth import as_jwt, auth_required

from ..model.user import User
from ..database.user_dao import UserDAO

import re


users_bp = Blueprint('users', __name__)


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
    dao = UserDAO()
    user = dao.find_one({"username": username})
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
    dao = UserDAO()
    users = dao.find_all_users(as_json=True)
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

    email_regex = r'[A-Za-z][A-Za-z0-9_.]*@[A-Za-z0-9_]+\.[A-Za-z0-9_]'
    email_format = lambda x: re.match(email_regex, x)
    validator.field_predicate(
        "email", email_format,
        mk_error("Incorrect email format")
    )

    # If there was an error, send response
    error_res = validator.error()
    if error_res is not None:
        return error_res

    new_user = User(
        username=body["username"],
        email=body["email"],
        password=body["password"]
    )
    dao = UserDAO()

    if dao.does_username_or_email_exist(body["username"], body["email"]):
        return mk_error("User with given name or email already exists.")
    else:
        dao.insert_one(new_user)

    return jsonify(new_user.as_dict())
