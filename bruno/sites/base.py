from flask import Blueprint, render_template
from .accounts import site as accounts_site
from flask_login.utils import login_required
from bruno.database.interaction.base import get_active_games
from bruno.forms.base import CreateGameForm

site = Blueprint("sites", __name__,
                 template_folder="templates", url_prefix="/")
site.register_blueprint(accounts_site)


@site.get("/")
def index():
    return render_template("index.html")


@site.get("/games/")
@login_required
def games():
    games = get_active_games()

    create_game_form = CreateGameForm()
    # TODO wtforms
    return render_template("games.html", games=games, create_game_form=create_game_form)
