import json

from flask import Blueprint, g, request

from models.category import Category
from utils.config import IMAGE_FILE_FORMATS
from utils.exceptions import ResponseException, NotFoundException, AlreadyExistsException
from utils import make_response, orm_list_with_pages
from utils import orm_to_dict
from utils.storage import allowed_file, save_file

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
                    'title', 'image_path', 'parent_id',
                ]
            ),
            query=items,
            page=request.args.get('_page')
        ),
    )


@bp.post('')
def index_post():
    form = json.loads(request.form['_json'])

    title = form['title']
    parent_id = form['parent_id'] or None
    image_file = request.files.get('image_file')

    parent = None
    image_path = None

    if parent_id:
        parent = g.db.query(Category).filter(
            Category.parent_id == parent_id
        ).first()

        if not parent:
            raise NotFoundException(payload={'code': 'parent_category_not_found'})

    if g.db.query(Category).filter(Category.title == title).first() is not None:
        raise AlreadyExistsException(payload={'code': 'title_already_exists'})

    if image_file:
        if image_file and allowed_file(image_file.filename, allowed_extensions=IMAGE_FILE_FORMATS):
            image_path = save_file(image_file, 'images')
        else:
            raise ResponseException(status='unsupported_image')

    item = Category(
        title=title,
        image_path=image_path or None,
        parent_id=parent.id if parent else None,
    )
    g.db.add(item)
    g.db.commit()

    return make_response(
        payload=orm_to_dict(
            item, ['title', 'image_path', 'parent_id'],
        ),
        status_code=201,
    )
