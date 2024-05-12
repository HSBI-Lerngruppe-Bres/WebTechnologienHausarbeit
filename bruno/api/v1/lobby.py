from flask import Blueprint, current_app, jsonify
from flask_login import login_required, current_user
from hashids import Hashids
from bruno.database.interaction.game import get_players_by_game_id, update_player_activity

api = Blueprint('lobby', __name__, url_prefix="/lobby")


@api.route("/state/<string:hashed_game_id>")
@login_required
def lobby_state(hashed_game_id):
    #TODO check if player in game
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)
    players = get_players_by_game_id(game_id)
    players_data = [{'name': player.name, 'id': player.id}
                    for player in players]
    game_info = {
        'game_id': game_id,
        'players': players_data,
    }
    update_player_activity(current_user.id)
    return jsonify(game_info)
