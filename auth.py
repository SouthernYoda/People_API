from connexion.decorators.security import validate_scope
from connexion.exceptions import OAuthScopeProblem

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

def dummy_function(token):
    return None

def get_secret(user) -> str:
    return f"you are {user} and the secret is a secret"
