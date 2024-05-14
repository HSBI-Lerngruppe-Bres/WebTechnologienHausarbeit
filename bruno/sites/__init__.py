from bruno.database.interaction import check_player_in_game, game_has_password, check_game, check_game_password, get_active_games, create_games, create_player_database, check_owner
from flask_login import login_required
from flask import Blueprint, render_template, current_app
from flask import Blueprint, render_template, redirect, url_for, current_app, request, flash
from flask_login.utils import login_required, current_user
from bruno.forms import CreateGameForm, JoinGameForm, CreatePlayerForm, GamePasswordForm
from hashids import Hashids
from flask_login import logout_user, login_user

site = Blueprint("sites", __name__,
                 template_folder="templates", url_prefix="/")


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
            return redirect(url_for('sites.join', hashed_game_id=hashids.encode(game.id)))
    elif 'join_game_submit' in request.form and join_game_form.validate_on_submit():
        return redirect(url_for('sites.join', hashed_game_id=join_game_form.hashed_game_id.data))

    return render_template("games.html", games=games, create_game_form=create_game_form, join_game_form=join_game_form)


@site.route('/create_player', methods=['GET', 'POST'])
def create_player():
    """The login and register handler for post and get request. Using
       WTForms to validate the players input. login or register the player

    Returns:
        HTTPResponse: Either the side the player wants to be redirected to or the login and register form
    """
    create_player_form = CreatePlayerForm(prefix='create_player')
    player = None
    if request.form and create_player_form.validate_on_submit():
        player = create_player_database(create_player_form.name.data)
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


@site.route('/join/<string:hashed_game_id>', methods=['GET', 'POST'])
@login_required
def join(hashed_game_id):
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)[0] if len(hashids.decode(
        hashed_game_id)) > 0 else None
    if not game_id or not check_game(game_id) or check_player_in_game(current_user):
        flash("The game does not exist or u are already in a game.")
        return redirect(url_for("sites.index"))
    if game_has_password(game_id) and not check_owner(game_id, current_user):
        game_password_form = GamePasswordForm()
        if not (game_password_form.validate_on_submit() and check_game_password(game_id, game_password_form.password.data)):
            return render_template("password.html", hashed_game_id=hashed_game_id, game_password_form=game_password_form)
    return render_template("lobby.html", hashed_game_id=hashed_game_id)


@site.route('/game/<string:hashed_game_id>', methods=['GET', 'POST'])
@login_required
def game(hashed_game_id):
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)[0] if len(hashids.decode(
        hashed_game_id)) > 0 else None
    if not game_id or not check_game(game_id) or check_player_in_game(current_user):
        flash("The game does not exist or u are already in a game.")
        return redirect(url_for("sites.index"))
    check_player_in_game(game_id, current_user)
    return render_template("game.html", hashed_game_id=hashed_game_id)
