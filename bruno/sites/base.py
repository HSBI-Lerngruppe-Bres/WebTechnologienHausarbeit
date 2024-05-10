from flask import Blueprint, render_template, redirect, url_for, current_app
from .accounts import site as accounts_site
from .game import site as game_site
from flask_login.utils import login_required, current_user
from bruno.database.interaction.base import get_active_games, create_games
from bruno.forms.base import CreateGameForm
from hashids import Hashids

site = Blueprint("sites", __name__,
                 template_folder="templates", url_prefix="/")
site.register_blueprint(accounts_site)
site.register_blueprint(game_site)


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
        hashids = Hashids(salt=current_app.config.get(
            "SECRET_KEY"), min_length=5)

        return redirect(url_for('sites.game.join', hashed_game_id=hashids.decode(game.id)))

    return render_template("games.html", games=games, create_game_form=create_game_form)
