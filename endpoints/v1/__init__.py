from flask import Blueprint

from utils import make_response
from endpoints.v1 import auth, category, product, office

bp = Blueprint('v1', __name__, url_prefix='/v1')

bp.register_blueprint(auth.bp)
bp.register_blueprint(category.bp)
bp.register_blueprint(product.bp)
bp.register_blueprint(office.bp)


@bp.get('')
def index_get():
    return make_response()
