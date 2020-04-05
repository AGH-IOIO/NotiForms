import os
import jwt

from functools import wraps

from flask import g, request, redirect, url_for

from flaskr.validate import mk_error

def as_jwt(dictionary):
    '''
    Data stored in this dictionary will be retrivable between requests.

    It should probably be some type of user identifier.
    '''
    return jwt.encode(
        dictionary,
        os.environ["JWT_SECRET"],
        algorithm="HS256"
    ).decode('utf-8')

def from_jwt(token):
    '''
    This function retrieves dictionary passed in mk_token.
    '''
    return jwt.decode(
        token,
        os.environ["JWT_SECRET"],
        algorithms=["HS256"]
    )

def auth_required(f):
    '''
    Handler decorator.
    Enforces valid JWT token in 'Authorization' header.

    If token sucessfully decoded, decrypted value will be available under g.session.
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        # Read 'Authorization' header
        token = request.headers.get("Authorization", None)
        if token is None:
            return mk_error("No authorization token provided.", code=401)()

        # Try to decode the token
        try:
            g.session = from_jwt(token)
        except Exception:
            return mk_error("Unable to devode provided token.", code=400)()

        return f(*args, **kwargs)

    return decorated
