from flask import Blueprint

bp = Blueprint('users', __name__)

from flaskr.users import handlers
