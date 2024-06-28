from flask import Blueprint

from controllers.auth import auth_required
from models.user import AVAILABLE_USER_ROLES
from utils import make_response
from endpoints.v1 import auth, category, product

bp = Blueprint('office', __name__, url_prefix='/office')

# bp.register_blueprint(auth.bp)


@bp.get('')
@auth_required(AVAILABLE_USER_ROLES)
def index_get():
    return make_response()
