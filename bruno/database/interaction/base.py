from bruno.database.models import Game, players_games
from bruno.database import db
from sqlalchemy import func
from typing import List, Optional
from ..models import User
from werkzeug.security import generate_password_hash
from flask import flash


def get_active_games() -> List[Game]:
    """Returns all active games

    Returns:
        List[Game]: The list of active games
    """
    active_games = db.session.query(
        Game.name,
        Game.id,
        Game.password_hash,
        func.count(players_games.c.user_id).label('player_count')
    ).where(
        Game.public == 0
    ).outerjoin(
        players_games, players_games.c.game_id == Game.id
    ).group_by(
        Game.id
    ).all()
    db.session.commit()
    return active_games


def create_games(game_name: str, public: bool, password: str, owner: User) -> Optional[Game]:
    """Create a game by the inputs of the form

    Args:
        game_name (str): The game_name from the form
        public (bool): If the game is public from the form
        password (str): The games password from the form
        owner (User): The games owner

    Returns:
        Optional[Game]: The created game
    """
    try:
        new_game = Game(
            name=game_name,
            owner_id=owner.id,
            public=0 if public else 1,
            password_hash=generate_password_hash(
                password) if password else None
        )
        db.session.add(new_game)
        db.session.commit()
        return new_game
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to create game: {e}")
        return None
