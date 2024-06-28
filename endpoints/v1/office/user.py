from flask import Blueprint, g

from controllers.auth import auth_required
from models.user import AVAILABLE_USER_ROLES
from utils import make_response, orm_to_dict

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.get('')
@auth_required(AVAILABLE_USER_ROLES)
def index_get():
    return make_response(orm_to_dict(
        g.user,
        [
            'phone_number', 'full_name', 'role'
        ],
    ))
