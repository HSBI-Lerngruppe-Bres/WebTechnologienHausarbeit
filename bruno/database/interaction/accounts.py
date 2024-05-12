from bruno.database.models import User
from flask import flash
from bruno.database import db
from typing import Optional


def create_user(username: str) -> Optional[User]:
    """Adds a new user to the database

    Args:
        username (str): The username from the form

    Returns:
        Optional[User]: The user object from the database
    """
    if not username:
        return None

    new_user = User(username=username)
    db.session.add(new_user)
    try:
        db.session.commit()
        flash(f"Created user: {username}", 'info')
        return new_user
    except Exception as e:
        db.session.rollback()
        flash(f"Error creating user: {e}", 'danger')
        return None
