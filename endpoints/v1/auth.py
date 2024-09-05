from flask import Blueprint, g, request

from utils.exceptions import ResponseException
from utils import make_response
from controllers.auth import create_access_token, check_password
from models.user import User
from utils import orm_to_dict

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.post('')
def index_post():
    phone_number = request.json['phone_number']
    password = request.json['password']

    user = g.db.query(User).filter(
        User.phone_number == phone_number,
        User.provider_name.is_(None),
    ).one()

    if check_password(password, user.encrypted_password) is False:
        raise ResponseException(status='wrong_password', status_code=400)

    return make_response({
        'user': orm_to_dict(
            user,
            [
                'phone_number', 'full_name', 'role'
            ],
        ),
        'token': create_access_token({'id': user.id}),
    })
