from flask import Blueprint

from utils import make_response
from endpoints.v1 import auth

bp = Blueprint('v1', __name__, url_prefix='/v1')

bp.register_blueprint(auth.bp)


@bp.get('')
def index_get():
    return make_response()
