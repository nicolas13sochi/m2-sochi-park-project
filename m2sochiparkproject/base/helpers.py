import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.http import HttpRequest
from django.contrib.auth import update_session_auth_hash
from importlib import import_module
from django.conf import settings
import random
from datetime import datetime, timedelta, timezone
from django.contrib.auth import get_user_model

User = get_user_model()


def init_session(session_key):
    """
    Initialize same session as done for ``SessionMiddleware``.
    """
    engine = import_module(settings.SESSION_ENGINE)
    return engine.SessionStore(session_key)

def logout_users():
    """
    Read all available users and all available not expired sessions. Then
    logout from each session.
    """
    request = HttpRequest()

    sessions = Session.objects.all()
    users = User.objects.all()

    for session in sessions:
        username = session.get_decoded().get('_auth_user_id')
        try:
            user = users.get(id=username)
        except Exception as err:
            print(err)
            continue
        else:
            request.session = init_session(session.session_key)
            request.user = user
            update_session_auth_hash(request, user)
            print(username)

    print('All OK!')


def generate_confirmation_code() -> int:
    return random.randint(100000, 999999)


def get_datetime_now_tz(delta=None):
    if delta is not None:
        return datetime.now(timezone.utc) + timedelta(seconds=delta)
    return datetime.now(timezone.utc)
