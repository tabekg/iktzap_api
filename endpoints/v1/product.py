import json

from flask import Blueprint, g, request

from models.category import Category
from models.product import Product
from utils.config import IMAGE_FILE_FORMATS
from utils.exceptions import ResponseException, AlreadyExistsException
from utils import make_response, orm_list_with_pages
from utils import orm_to_dict
from utils.storage import allowed_file, save_file

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.get('')
def index_get():
    category_id = request.args.get('category_id')

    items = g.db.query(Product)

    if category_id:
        category = g.db.query(Category).filter(Category.id == category_id).one()
        items = items.filter(Product.category_id == category.id)

    items = items.order_by(Product.id.desc())

    return make_response(
        orm_list_with_pages(
            render=lambda c: orm_to_dict(
                c.all(),
                [
                    'title', 'description', 'price',
                    'image_path', 'in_stock',
                    'category_id',
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
    description = form['description']
    price = form['price']
    in_stock = form['in_stock']
    category_id = form['category_id']
    image_file = request.files.get('image_file')

    category = g.db.query(Category).filter(Category.id == category_id).one()

    image_path = None

    if g.db.query(Product).filter(Product.title == title).first() is not None:
        raise AlreadyExistsException(payload={'code': 'title_already_exists'})

    if image_file:
        if image_file and allowed_file(image_file.filename, allowed_extensions=IMAGE_FILE_FORMATS):
            image_path = save_file(image_file, 'images')
        else:
            raise ResponseException(status='unsupported_image')

    item = Product(
        title=title,
        description=description,
        price=price,
        image_path=image_path or None,
        in_stock=in_stock,
        category_id=category.id,
    )
    g.db.add(item)
    g.db.commit()

    return make_response(
        payload=orm_to_dict(
            item,
            [
                'title', 'description', 'price',
                'image_path', 'in_stock',
                'category_id',
            ],
        ),
        status_code=201,
    )
