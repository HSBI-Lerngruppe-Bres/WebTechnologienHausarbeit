from flask import Blueprint,render_template
from .accounts import site as accounts_site
from flask_login.utils import login_required

site = Blueprint("sites", __name__, template_folder="templates", url_prefix="/")
site.register_blueprint(accounts_site)

@site.get("/")
def index():
    return render_template("index.html")

@site.get("/games/")
@login_required
def games():
    games = [
        {'name': "Mark's Game", 'player_count': 4, 'protection': 2},
        {'name': "John's Game", 'player_count': 12, 'protection': 1},
        {'name': "Jane's Game", 'player_count': 6, 'protection': 0}
    ]
    return render_template("games.html", games=games)