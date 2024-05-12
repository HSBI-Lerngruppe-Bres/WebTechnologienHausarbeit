import os
import logging
from flask import Flask
from flask_login import LoginManager
from pathlib import Path
from flask_migrate import Migrate
from .database.models import Player


def create_app():
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
        # TODO Maybe split into multiple functions and files

    logging.debug(f"Initialize database")
    from .database import db
    db.init_app(app)
    Migrate(app, db)

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'sites.choose_name'

    @login_manager.user_loader
    def user_loader(player_id):
        return Player.query.get(player_id)

    from .sites.base import site as base_site
    app.register_blueprint(base_site)

    # TODO Logging stuff
    return app
