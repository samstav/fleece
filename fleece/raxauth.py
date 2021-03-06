import requests

from httperror import HTTPError


def authenticate():
    def wrap(fxn):
        """Return a decorated callable."""
        def wrapped(*args, **kwargs):
            """Validate token and return auth context."""
            if 'token' not in kwargs:
                raise HTTPError(status=401)
            validate(kwargs['token'])
            return fxn(*args, **kwargs)
        return wrapped
    return wrap


def validate(token):
    """Validate token and return auth context."""
    endpoint = 'identity.api.rackspacecloud.com'
    auth_url = "https://%s/v2.0/tokens/%s" % (endpoint, token)
    headers = {
        'x-auth-token': token,
        'accept': 'application/json',
    }
    resp = requests.get(auth_url, headers=headers)

    if not resp.status_code == 200:
        raise HTTPError(status=resp.status_code)
    return
