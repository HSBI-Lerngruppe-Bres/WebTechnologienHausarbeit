from flask import Blueprint
from .game import api as game_api
from .lobby import api as lobby_api

api = Blueprint('v1', __name__, url_prefix="/v1")

api.register_blueprint(game_api)
api.register_blueprint(lobby_api)
