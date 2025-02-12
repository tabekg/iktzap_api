import json

from flask import Blueprint, g, request

from controllers.auth import auth_required
from models.category import Category
from models.product import Product
from models.user import UserRoleEnum
from utils.config import IMAGE_FILE_EXTENSIONS
from utils.exceptions import ResponseException, NotFoundException, AlreadyExistsException
from utils import make_response, orm_list_with_pages
from utils import orm_to_dict
from utils.storage import allowed_file, save_file, delete_file

bp = Blueprint('category', __name__, url_prefix='/category')


@bp.get('')
def index_get():
    parent_id = request.args.get('parent_id') or None
    id_ = request.args.get('id') or None

    assert id_ is None or parent_id is None

    items = g.db.query(Category)

    if parent_id:
        items = items.filter(Category.parent_id == parent_id)
    elif id_:
        items = items.filter(Category.id == id_)
    else:
        items = items.filter(Category.parent_id.is_(None))

    if id_:
        return make_response(
            orm_to_dict(
                items.one(),
                [
                    'title', 'image_path', 'parent_id',
                    'updated_at',
                ]
            )
        )

    return make_response(
        orm_list_with_pages(
            render=lambda c: orm_to_dict(
                c.all(),
                [
                    'title', 'image_path', 'parent_id',
                    'updated_at',
                ]
            ),
            query=items.order_by(Category.title.asc()),
            page=request.args.get('_page')
        ),
    )


@bp.get('/all')
def all_get():
    items = g.db.query(Category)

    return make_response(
        orm_list_with_pages(
            render=lambda c: orm_to_dict(
                c.all(),
                [
                    'title', 'image_path', 'parent_id',
                    'updated_at',
                ]
            ),
            query=items.order_by(Category.title.asc()),
            page=request.args.get('_page')
        ),
    )


@bp.delete('')
@auth_required(UserRoleEnum.super_admin)
def index_delete():
    id_ = request.args['id']

    item = g.db.query(Category).filter(Category.id == id_).one()

    assert g.db.query(Category).filter(Category.parent_id == item.id).count() == 0
    assert g.db.query(Product).filter(Product.category_id == item.id).count() == 0

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
    parent_id = form['parent_id'] or None
    image_file = request.files.get('image_file')

    if id_:
        item = g.db.query(Category).filter(Category.id == id_).one()
    else:
        item = None

    parent = None
    image_path = None

    if parent_id:
        parent = g.db.query(Category).filter(
            Category.id == parent_id
        ).first()

        if not parent:
            raise NotFoundException(payload={'code': 'parent_category_not_found'})

    if item is None:
        if g.db.query(Category).filter(Category.title == title).first() is not None:
            raise AlreadyExistsException(payload={'code': 'title_already_exists'})
    else:
        if title != item.title and g.db.query(Category).filter(Category.title == title).first() is not None:
            raise AlreadyExistsException(payload={'code': 'title_already_exists'})

    if image_file:
        if allowed_file(image_file.filename, allowed_extensions=IMAGE_FILE_EXTENSIONS):
            image_path = save_file(image_file, 'images')
            if item and item.image_path:
                delete_file(item.image_path, 'images')
        else:
            raise ResponseException(status='unsupported_image')

    if item is None:
        item = Category(
            title=title,
            image_path=image_path or None,
            parent_id=parent.id if parent else None,
        )
        g.db.add(item)
    else:
        item.title = title
        item.image_path = image_path or None if image_file else item.image_path
        item.parent_id = parent.id if parent else None

    g.db.commit()

    return make_response(
        payload=orm_to_dict(
            item, ['title', 'image_path', 'parent_id', 'updated_at'],
        ),
        status_code=200 if id_ else 201,
    )
