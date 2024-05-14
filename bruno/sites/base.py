from flask import Blueprint, render_template, redirect, url_for, current_app, request, flash
from .game import site as game_site
from flask_login.utils import login_required, current_user
from bruno.database.interaction.base import get_active_games, create_games, create_player
from bruno.forms.base import CreateGameForm, JoinGameForm, CreatePlayerForm
from hashids import Hashids
from flask_login import logout_user, login_user

site = Blueprint("sites", __name__,
                 template_folder="templates", url_prefix="/")

site.register_blueprint(game_site)


@site.get("/")
def index():
    return render_template("index.html")


@site.route("/games/", methods=["GET", "POST"])
@login_required
def games():
    games = get_active_games()
    create_game_form = CreateGameForm(name=current_user.name)
    join_game_form = JoinGameForm()
    if 'create_game_submit' in request.form and create_game_form.validate_on_submit():
        game = create_games(create_game_form.game_name.data,
                            create_game_form.public.data,
                            create_game_form.password.data,
                            current_user)
        hashids = Hashids(salt=current_app.config.get(
            "SECRET_KEY"), min_length=5)
        if game:
            return redirect(url_for('sites.game.join', hashed_game_id=hashids.encode(game.id)))
    elif 'join_game_submit' in request.form and join_game_form.validate_on_submit():
        return redirect(url_for('sites.game.join', hashed_game_id=join_game_form.hashed_game_id.data))

    return render_template("games.html", games=games, create_game_form=create_game_form, join_game_form=join_game_form)


@site.route('/choose_name', methods=['GET', 'POST'])
def choose_name():
    """The login and register handler for post and get request. Using
       WTForms to validate the players input. login or register the player

    Returns:
        HTTPResponse: Either the side the player wants to be redirected to or the login and register form
    """
    # TODO redirect after logged in
    create_player_form = CreatePlayerForm(prefix='create_player')
    player = None
    if request.form and create_player_form.validate_on_submit():
        player = create_player(create_player_form.name.data)
    if player:
        login_user(player)
        next = request.args.get('next')
        # TODO possible security risk
        return redirect(next or url_for('sites.index'))
    return render_template('create_player.html', create_player_form=create_player_form)


@site.get("/logout")
def logout():
    """Listens to /logout via get and logs the player out.

    Returns:
        HTTPResponse: The redirect to the index page
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('sites.index'))
