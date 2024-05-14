from flask import Blueprint, render_template, current_app
from flask_login import login_required
from hashids import Hashids
from bruno.database.interaction import get_players_by_game_id, game_has_password, check_game_password
from bruno.forms.base import GamePasswordForm

site = Blueprint("game", __name__,
                 template_folder="templates/game", url_prefix="/game")


@site.route('/join/<string:hashed_game_id>', methods=['GET', 'POST'])
@login_required
def join(hashed_game_id):
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)[0]
    # TODO check for not valid game id
    # TODO check if user is owner then no password
    # TODO redirect if no game
    # TODO check if player in game
    if game_has_password(game_id):
        game_password_form = GamePasswordForm()
        if not (game_password_form.validate_on_submit() and check_game_password(game_id, game_password_form.password.data)):
            return render_template("password.html", hashed_game_id=hashed_game_id, game_password_form=game_password_form)
    players = get_players_by_game_id(game_id)
    return render_template("lobby.html", hashed_game_id=hashed_game_id)


@site.route('/game/<string:hashed_game_id>', methods=['GET', 'POST'])
@login_required
def game(hashed_game_id):
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)[0]
    # TODO check if player in game
    return render_template("game.html", hashed_game_id=hashed_game_id)
