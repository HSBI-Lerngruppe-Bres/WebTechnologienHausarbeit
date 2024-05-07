import os
import logging
from flask import Flask
#from flask_login import LoginManager
from pathlib import Path
from flask_migrate import Migrate


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
        #TODO Handle other Debug stuff
        #TODO Maybe split into multiple functions and files


    logging.debug(f"Initialize database")
    from .database import db
    db.init_app(app)
    Migrate(app, db)

    """# Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'site.login'

    @login_manager.user_loader  
    def user_loader(user_id):
        return User.query.get(user_id)
    """

    """with app.app_context():
        db.create_all()
        NEW_DB = all(db.session.query(table).first()
                     is None for table in db.metadata.sorted_tables)

        if NEW_DB:
            logging.info("All tables are empty. Seeding database...")
            seed_database()"""

    from .sites.base import site as base_site
    app.register_blueprint(base_site)

    # logging.info(app.config)

    return app