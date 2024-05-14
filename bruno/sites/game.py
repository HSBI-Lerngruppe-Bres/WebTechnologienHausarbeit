from flask import Blueprint, render_template, current_app
from flask_login import login_required
from hashids import Hashids
from bruno.database.interaction.game import get_players_by_game_id, check_game_join

site = Blueprint("game", __name__,
                 template_folder="templates/game", url_prefix="/game")


@site.route('/join/<string:hashed_game_id>', methods=['GET', 'POST'])
@login_required
def join(hashed_game_id):
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)[0]
    # TODO redirect or password requesr
    # TODO redirect if no game
    # TODO check if player in game
    players = get_players_by_game_id(game_id)
    return render_template("lobby.html", hashed_game_id=hashed_game_id)


@site.route('/game/<string:hashed_game_id>', methods=['GET', 'POST'])
@login_required
def game(hashed_game_id):
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)[0]
    # TODO check if player in game
    # TODO check if game started
    return render_template("game.html", hashed_game_id=hashed_game_id)
