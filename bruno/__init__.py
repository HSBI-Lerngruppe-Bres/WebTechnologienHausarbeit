import os
import logging
from flask import Flask
from flask_login import LoginManager
from pathlib import Path
from flask_migrate import Migrate
from .database.models import Player
from flask_socketio import SocketIO
from .database import db
from .socketio import GameNamespace
from .sites import site as base_site

# from .database.interaction import remove_inactive_players, remove_inactive_players_from_game
# from datetime import timedelta
# from flask_apscheduler import APScheduler
# def remove_inactive_players_periodically(app: Flask):
#    """Periodicly runs to remove the inactive Players
#    """
#    with app.app_context():
#        timeout_remove = timedelta(minutes=15)
#        timeout_leave = timedelta(seconds=20)
#        remove_inactive_players(timeout_remove)
#        remove_inactive_players_from_game(timeout_leave)


def create_app() -> Flask:
    """Creates the flask app

    Returns:
        Flask: The flask app
    """
    # TODO Maybe split into multiple functions and files

    logging.basicConfig(level=logging.INFO)
    logging.info(f"Creating app")

    INSTANCE_PATH = os.path.abspath(os.path.join(
        os.path.abspath(__path__[0]), "../instance"))
    app = Flask(__name__, instance_path=INSTANCE_PATH)
    logging.info(f"Created app at: {INSTANCE_PATH}")

    CONFIG_PATH = Path(app.instance_path) / 'config.cfg'
    if CONFIG_PATH.is_file():
        app.config.from_pyfile(str(CONFIG_PATH))
        logging.info(f"Loaded config from: {CONFIG_PATH}")
    else:
        logging.warning(
            f"Configuration file not found at {CONFIG_PATH}")

    if app.config.get('DEBUG', False):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug(f"App created in debug mode at: {INSTANCE_PATH}")
        # TODO Handle other Debug stuff

    logging.debug(f"Initialize database")
    db.init_app(app)
    Migrate(app, db)

    # Setup Flask-Login
    logging.debug(f"Setup Flask-Login")
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'sites.choose_name'

    @login_manager.user_loader
    def user_loader(player_id):
        return Player.query.get(player_id)

    logging.debug(f"Setup blueprints")
    app.register_blueprint(base_site)

    # TODO Logging stuff

    # Setup removal of inactive players
    """logging.debug(f"Setup removal of inactive players")
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='Removal of inactive players', func=remove_inactive_players_periodically, args=[app],
                      trigger='interval', seconds=10)"""
    return app


def create_socketio(app: Flask) -> SocketIO:
    logging.debug(f"Setup Flask-SocketIO")
    socketio = SocketIO()
    socketio.init_app(app)
    socketio.on_namespace(GameNamespace('/game'))
    return socketio
