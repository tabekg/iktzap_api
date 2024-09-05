from datetime import datetime, timezone, timedelta
from functools import wraps

import bcrypt
import jwt
from flask import request, g

from models.user import User
from utils.exceptions import ResponseException
from utils.config import ACCESS_TOKEN_EXPIRE_DAYS, SECRET_KEY


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def create_access_token(data):
    return jwt.encode({
        **data,
        'iss': 'besoft:iktzap',
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    }, SECRET_KEY, algorithm="HS256")


def get_hashed_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_auth_token():
    token = request.headers['Authorization'][7:] if 'Authorization' in request.headers else None
    try:
        if not token:
            g.user = None
        else:
            data = jwt.decode(
                token,
                SECRET_KEY,
                options={"require": ["exp", "iss"]},
                issuer='besoft:iktzap',
                algorithms=["HS256"],
            )
            g.user = g.db.query(User) \
                .filter_by(id=data['id'], provider_name=None) \
                .first()
            if g.user and g.user.is_disabled is True:
                g.user = None
    except Exception as e:
        raise ResponseException(payload=str(e), status='token_is_invalid', status_code=401)


def check_user(roles=None):
    if request.method == 'OPTIONS':
        return
    check_auth_token()
    if not hasattr(g, 'user') or not g.user:
        raise ResponseException(payload='User not authorized', status='not_authorized', status_code=401)
    if roles is not None and g.user.role not in roles:
        raise ResponseException(payload='The user has no permission', status='access_denied', status_code=403)


def auth_required(roles=None):
    def wrapper(fn):
        @wraps(fn)
        def wrapped_function(*args, **kwargs):
            check_user(roles=roles)
            return fn(*args, **kwargs)

        return wrapped_function

    return wrapper
