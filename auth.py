from connexion.decorators.security import validate_scope
from connexion.exceptions import OAuthScopeProblem

import six
from jose import JWTError, jwt
from datetime import datetime, timedelta


JWT_ISSUER = 'com.people.connexion'
JWT_SECRET = 'change_this'
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'

def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        six.raise_from(Unauthorized, e)

def generate_token():
    user_id = 1

    timestamp = datetime.utcnow()

    payload = {
        "iss": JWT_ISSUER,
        "iat": timestamp,
        "exp": timestamp + timedelta(seconds=JWT_LIFETIME_SECONDS),
        "sub": str(user_id),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def basic_auth(username, password, required_scopes=None):
    if username == 'admin' and password == 'secret':
        info = {'sub': 'admin', "scope": "secret"}
    elif username == "foo" and password == "bar":
        info = {'sub': "user1", "scope": ""}
    else:
        return None

    # optional
    if required_scopes is not None and not validate_scope(required_scopes, info['scope']):
        raise OAuthScopeProblem(
            description="Provided user doesn\'t have the required access rights",
            required_scopes=required_scopes,
            token_scopes=info['scope']
        )

    return info

def get_secret(user) -> str:
    return f"you are {user} and the secret is a secret"
