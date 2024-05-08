from bruno.database.models import Game, players_games
from bruno.database import db
from sqlalchemy import func

def get_active_games():
    active_games = db.session.query(
        Game.title,
        Game.protection,
        func.count(players_games.c.user_id).label('player_count')
    ).join(
        players_games, players_games.c.game_id == Game.id
    ).group_by(
        Game.id
    ).all()
    
    return active_games