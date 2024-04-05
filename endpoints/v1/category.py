from flask import Blueprint, g, request

from models.category import Category
from utils.exceptions import ResponseException
from utils import make_response, orm_list_with_pages
from controllers.auth import create_access_token, check_password
from models.user import User
from utils import orm_to_dict

bp = Blueprint('category', __name__, url_prefix='/category')


@bp.get('')
def index_get():
    parent_id = request.args.get('parent_id') or None

    items = g.db.query(Category)

    if parent_id:
        items = items.filter(Category.parent_id == parent_id)
    else:
        items = items.filter(Category.parent_id.is_(None))

    return make_response(
        orm_list_with_pages(
            render=lambda c: orm_to_dict(
                c.all(),
                [
                    'title', 'image_path',
                ],
                {
                    'parent': lambda a: orm_to_dict(a.parent, [
                        'title', 'image_path'
                    ]),
                }
            ),
            query=items,
            page=request.args.get('_page')
        ),
    )


@bp.post('')
def index_post():
    phone_number = request.json['phone_number']
    password = request.json['password']

    user = g.db.query(User).filter(
        User.phone_number == phone_number,
        User.provider_name == 'phone_number',
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
        'token': create_access_token({'phone_number': user.phone_number}),
    })
