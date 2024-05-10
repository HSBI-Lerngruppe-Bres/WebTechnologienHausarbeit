from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from bruno.database.models import User
from flask import flash
from bruno.database import db
from typing import Optional


def authenticate_user(username: str, password: str) -> Optional < User >:
    """Validates the credentials of a user by its username and password

    Args:
        username (str): The username from the form
        password (str): The password from the form

    Returns:
        Optional(User): The user object from the database
    """
    try:
        user: User = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        flash(f'Invalid username or password', 'danger')
        return None
    except Exception as e:
        flash(f"{e}", 'danger')
        return None


def register_user(username: str, password: str, password_confirmed: str, email: str):
    # TODO implement password confirm
    # TODO implement Email
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
