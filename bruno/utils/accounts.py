from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from bruno.database.models import User
from flask import flash
from bruno.database import db

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
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    try:
        db.session.commit()
        flash(f"Created user: {username}", 'info')
        login_user(new_user)
        return True
    except Exception as e:
        db.session.rollback()
        flash(f"Error registering user: {e}", 'danger')
        return False