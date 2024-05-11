from flask import Blueprint, redirect, url_for, render_template, current_app
from flask_login import login_required
from hashids import Hashids

site = Blueprint("game", __name__,
                 template_folder="templates/game", url_prefix="/game")


@site.route('/join/<string:hashed_game_id>', methods=['GET', 'POST'])
@login_required
def join(hashed_game_id):
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)
    # TODO redirect or password requesr
    # TODO redirect if no game
    # Logic to add the current user to the game's players
    # Redirect to the game page or display some confirmation message
    return redirect(url_for('sites.game.lobby', hashed_game_id=hashed_game_id))


@site.route('/lobby/<string:hashed_game_id>', methods=['GET', 'POST'])
@login_required
def lobby(hashed_game_id):
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)
    # Logic to add the current user to the game's players
    # Redirect to the game page or display some confirmation message
    return render_template("lobby.html", hashed_game_id=hashed_game_id)
