from flask import Blueprint

from utils import make_response
from endpoints.v1 import auth, category, product

bp = Blueprint('office', __name__, url_prefix='/office')

# bp.register_blueprint(auth.bp)


@bp.get('')
def index_get():
    return make_response()