from typing import List
from ..models import Game, Player, db
from datetime import datetime, timezone, timedelta


def get_players_by_game_id(game_id: int) -> List[Player]:
    """
    Retrieve all players participating in a specific game by the game ID.

    Args:
        game_id (int): The ID of the game to retrieve players from.

    Returns:
        List[Player]: A list of Player objects that are players in the specified game.
    """
    game = Game.query.get(game_id)
    if game:
        return game.players
    return []


def player_join_game(player_id: int, game_id: int) -> bool:
    """
    Adds a player to a game based on provided player and game IDs.

    Args:
        player_id (int): The ID of the player to add to the game.
        game_id (int): The ID of the game to which the player will be added.

    Returns:
        bool: True if the player was successfully added to the game, False otherwise.
    """
    try:
        game = Game.query.get(game_id)
        player = Player.query.get(player_id)
        if not game or not player:
            print("Game or player not found.")
            return False
        if player in game.players:
            print("Player is already in the game.")
            return False
        game.players.append(player)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while adding player to game: {e}")
        return False


def update_player_activity(player_id: int):
    """Resets the players activity to the current

    Args:
        player_id (int): The id of the player
    """
    player = Player.query.filter_by(id=player_id).first()
    if player:
        player.last_active = datetime.now(timezone.utc)
    else:
        player = Player(id=player_id)
        db.session.add(player)
    db.session.commit()


def remove_inactive_players(timeout: timedelta):
    """Removes all inactive or disconnected players

    Args:
        timeout (timedelta): The timeout duration
    """
    timeout_threshold = datetime.now(timezone.utc) - timeout
    inactive_players = Player.query.filter(
        Player.last_active < timeout_threshold).all()
    for player in inactive_players:
        db.session.delete(player)
    db.session.commit()


def remove_inactive_players_from_game(timeout: timedelta):
    """
    Removes players from games who have been inactive longer than the specified timeout.

    Args:
        timeout (timedelta): The duration of time after which players are considered inactive.
    """
    now = datetime.now(timezone.utc)
    timeout_threshold = now - timeout
    inactive_players = Player.query.filter(
        Player.last_active < timeout_threshold).all()
    for player in inactive_players:
        for game in player.games:
            game.players.remove(player)
        db.session.commit()
