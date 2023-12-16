import pyrebase
from requests import HTTPError, RequestException

from trail.exception.auth import InvalidCredentialsException
from trail.exception.trail import TrailUnavailableException
from trail.libconfig import libconfig

_user_id_token = None


def authenticate(username, password):
    firebase = pyrebase.initialize_app(
        {
            "apiKey": libconfig.FIREBASE_API_KEY,
            "authDomain": libconfig.FIREBASE_AUTH_DOMAIN,
            "databaseURL": "THIS_IS_NOT_USED",
            "storageBucket": "THIS_IS_NOT_USED",
        }
    )
    auth = firebase.auth()

    try:
        user = auth.sign_in_with_email_and_password(username, password)
    except HTTPError as e:
        # workaround for pyrebase not raising the correct exception
        status_code = e.errno.response.status_code
        if status_code == 400:
            raise InvalidCredentialsException() from e

        raise TrailUnavailableException() from e
    except RequestException as e:
        raise TrailUnavailableException() from e

    return user["idToken"]


def retrieve_id_token() -> str:
    from trail.userconfig import userconfig
    global _user_id_token

    if not _user_id_token:
        _user_id_token = authenticate(userconfig().username, userconfig().password)

    return _user_id_token
