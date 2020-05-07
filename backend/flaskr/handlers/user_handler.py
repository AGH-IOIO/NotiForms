import os
import re

from flask import g, jsonify, Blueprint, url_for

from .. import app
from ..auth import as_jwt, auth_required
from ..database.unconfirmed_user_dao import UnconfirmedUserDAO
from ..database.user_dao import UserDAO
from ..email import send_email
from ..model.unconfirmed_user import UnconfirmedUser
from ..model.utils import create_user_registration_link
from ..validate import Validator, mk_error, expect_mime, json_body

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
    users = dao.find_all_users()
    users_data = [user.data for user in users]
    return jsonify({"users": users_data})


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

    new_user_data = {"username": body["username"],
                     "email": body["email"],
                     "password": body["password"]}

    unconfirmed_user_data = {"link": create_user_registration_link(
        new_user_data["username"]),
        "user": new_user_data}
    new_unconfirmed_user = UnconfirmedUser(unconfirmed_user_data)
    dao = UnconfirmedUserDAO()

    if dao.does_username_or_email_exist(body["username"], body["email"]):
        return mk_error("User with given name or email already exists.")
    else:
        dao.insert_one(new_unconfirmed_user)

        if os.environ["TEST"] != 'y':
            send_email(new_unconfirmed_user.email,
                       'Confirm your registration',
                       'registration_email',
                       username=new_unconfirmed_user.username,
                       link=new_unconfirmed_user.link)

    return jsonify(new_unconfirmed_user.data)


@app.route("/users/confirm/<token>/", methods=["POST"])
def confirm(token):
    from ..model.utils import confirm_user

    link = url_for('confirm', token=token, _external=True)
    if confirm_user(link=link):
        return jsonify({"confirmation": "OK"})
    else:
        return jsonify({"confirmation": "Error"})
    # TODO - redirect to main page


@app.route("/users/get_teams/<username>/", methods=["GET"])
@auth_required
def get_user_teams(username):
    user_dao = UserDAO()
    user = user_dao.find_one({"username": username})
    if user is None:
        return mk_error("User with given username does not exist!")

    teams = user.teams
    return jsonify({"teams": teams})
