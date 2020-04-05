import os
import jwt

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
