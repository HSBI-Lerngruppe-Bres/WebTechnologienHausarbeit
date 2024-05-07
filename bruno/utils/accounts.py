from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from bruno.database.models import User
from flask import flash

def authenticate_user(username, password):
    try:
        user: User = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return True
        flash(f'Invalid username or password', 'danger')
        return False
    except Exception as e:
        flash(f"{e}", 'danger')
        return False


def register_user(username, password):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("Name already taken", 'danger')
        return True
    User.createNew(username, generate_password_hash(password))
    return False