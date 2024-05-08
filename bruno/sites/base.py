from flask import Blueprint,render_template
from .accounts import site as accounts_site
from flask_login.utils import login_required
from bruno.utils.base import get_active_games

site = Blueprint("sites", __name__, template_folder="templates", url_prefix="/")
site.register_blueprint(accounts_site)

@site.get("/")
def index():
    return render_template("index.html")

@site.get("/games/")
@login_required
def games():
    games = get_active_games()
    print(games)
    #TODO wtforms
    return render_template("games.html", games=games)