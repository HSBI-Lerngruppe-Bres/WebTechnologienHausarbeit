from flask import Blueprint, current_app, jsonify
from flask_login import login_required, current_user
from hashids import Hashids
from bruno.database.interaction.game import get_players_by_game_id

api = Blueprint('lobby', __name__, url_prefix="/lobby")


@api.route("/state/<string:hashed_game_id>")
@login_required
def lobby_state(hashed_game_id):
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)
    players = get_players_by_game_id(game_id)
    players_data = [{'username': player.username, 'id': player.id}
                    for player in players]
    game_info = {
        'game_id': game_id,
        'players': players_data,
    }
    return jsonify(game_info)
