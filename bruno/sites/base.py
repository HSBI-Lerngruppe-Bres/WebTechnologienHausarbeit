from flask import Blueprint, render_template
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
    create_game_form = CreateGameForm()
    if create_game_form.validate_on_submit():
        print(create_games(create_game_form.game_name.data,
                           create_game_form.public.data,
                           create_game_form.password.data,
                           current_user))

    return render_template("games.html", games=games, create_game_form=create_game_form)
