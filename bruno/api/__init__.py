from flask import Blueprint
from .v1 import api as v1_bluetrint

api = Blueprint('api', __name__, url_prefix="/api")

api.register_blueprint(v1_bluetrint)
