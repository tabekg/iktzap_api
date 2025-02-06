import json

from flask import Blueprint, g, request

from controllers.auth import auth_required
from models.slide import Slide
from models.user import UserRoleEnum
from utils.config import IMAGE_FILE_EXTENSIONS
from utils.exceptions import ResponseException
from utils import make_response, orm_list_with_pages
from utils import orm_to_dict
from utils.storage import allowed_file, save_file, delete_file

bp = Blueprint('slide', __name__, url_prefix='/slide')


@bp.get('')
def index_get():
    items = g.db.query(Slide)

    return make_response(
        orm_list_with_pages(
            render=lambda c: orm_to_dict(
                c.all(),
                [
                    'title', 'image_path',
                ]
            ),
            query=items.order_by(Slide.id.desc()),
            page=request.args.get('_page')
        ),
    )


@bp.delete('')
@auth_required(UserRoleEnum.super_admin)
def index_delete():
    id_ = request.args['id']

    item = g.db.query(Slide).filter(Slide.id == id_).one()

    if item.image_path:
        delete_file(item.image_path, 'images')
    g.db.delete(item)
    g.db.commit()

    return make_response()


@bp.post('')
@auth_required(UserRoleEnum.super_admin)
def index_post():
    form = json.loads(request.form['_json'])

    id_ = form.get('id')
    title = form['title']
    image_file = request.files.get('image_file')

    if id_:
        item = g.db.query(Slide).filter(Slide.id == id_).one()
    else:
        item = None

    image_path = None

    if image_file:
        if allowed_file(image_file.filename, allowed_extensions=IMAGE_FILE_EXTENSIONS):
            image_path = save_file(image_file, 'images')
            if item and item.image_path:
                delete_file(item.image_path, 'images')
        else:
            raise ResponseException(status='unsupported_image')

    if item is None:
        item = Slide(
            title=title,
            image_path=image_path or None,
        )
        g.db.add(item)
    else:
        item.title = title
        item.image_path = image_path or None if image_file else item.image_path

    g.db.commit()

    return make_response(
        payload=orm_to_dict(
            item, ['title', 'image_path'],
        ),
        status_code=200 if id_ else 201,
    )
