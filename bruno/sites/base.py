from flask import Blueprint, render_template, redirect, url_for
from .accounts import site as accounts_site
from flask_login.utils import login_required, current_user
from bruno.database.interaction.base import get_active_games, create_games
from bruno.forms.base import CreateGameForm

site = Blueprint("sites", __name__,
                 template_folder="templates", url_prefix="/")
site.register_blueprint(accounts_site)


@site.get("/")
def index():
    return render_template("index.html")


@site.route("/games/", methods=["GET", "POST"])
@login_required
def games():
    games = get_active_games()
    create_game_form = CreateGameForm(username=current_user.username)
    if create_game_form.validate_on_submit():
        game = create_games(create_game_form.game_name.data,
                            create_game_form.public.data,
                            create_game_form.password.data,
                            current_user)
        return redirect(url_for('sites.join_game', game_id=game.id))

    return render_template("games.html", games=games, create_game_form=create_game_form)


@site.route('/game/join/<int:game_id>', methods=['GET', 'POST'])
@login_required
def join_game(game_id):
    # TODO redirect or password requesr
    # Logic to add the current user to the game's players
    # Redirect to the game page or display some confirmation message
    return redirect(url_for('sites.game_lobby', game_id=game_id))


@site.route('/game/lobby/<int:game_id>', methods=['GET', 'POST'])
@login_required
def game_lobby(game_id):
    # Logic to add the current user to the game's players
    # Redirect to the game page or display some confirmation message
    return render_template("game_lobby.html")
