from flask import Blueprint, g, request

from utils.exceptions import ResponseException
from utils import make_response
from controllers.auth import create_access_token, check_password, auth_required, get_hashed_password
from models.user import User
from utils import orm_to_dict

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.post('')
def index_post():
    login = request.json['login']
    password = request.json['password']

    user = g.db.query(User).filter(
        User.provider_uid == login,
        User.provider_name == 'login',
    ).one()

    if check_password(password, user.encrypted_password) is False:
        raise ResponseException(status='wrong_password', status_code=400)

    return make_response({
        'user': orm_to_dict(
            user,
            [
                'provider_name', 'provider_uid', 'provider_id',
                'phone_number', 'full_name', 'role'
            ],
        ),
        'token': create_access_token({'id': user.id}),
    })


@bp.post('/password')
@auth_required()
def password_post():
    current = request.json['current']
    new = request.json['new']

    assert 0 < len(new) < 20

    if check_password(current, g.user.encrypted_password) is False:
        raise ResponseException(status='wrong_password', status_code=400)

    g.user.encrypted_password = get_hashed_password(new)
    g.db.commit()

    return make_response()
