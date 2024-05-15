from .models import Game, Player, db
from werkzeug.security import check_password_hash
from bruno.database.models import Game
from bruno.database import db
from sqlalchemy import func
from typing import List, Optional
from .models import Player
from werkzeug.security import generate_password_hash
from flask import flash, current_app
from hashids import Hashids


def get_active_games() -> List[dict]:
    """Returns all active games with encoded IDs

    Returns:
        List[dict]: The list of active games with encoded IDs
    """
    active_games_query = db.session.query(
        Game.name,
        Game.id,
        Game.password_hash,
        func.count(Player.id).label('player_count')
    ).filter(
        Game.public == 0
    ).outerjoin(
        Player, Player.game_id == Game.id
    ).group_by(
        Game.id
    ).all()

    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    active_games = [
        {
            'name': game.name,
            'hashed_game_id': hashids.encode(game.id),
            'player_count': game.player_count,
            'password_hash': game.password_hash
        } for game in active_games_query
    ]
    return active_games


def create_games(game_name: str, public: bool, password: str, owner: Player) -> Optional[Game]:
    """Create a game by the inputs of the form

    Args:
        game_name (str): The game_name from the form
        public (bool): If the game is public from the form
        password (str): The games password from the form
        owner (Player): The games owner

    Returns:
        Optional[Game]: The created game
    """
    try:
        new_game = Game(
            name=game_name,
            # owner_id=owner.id,
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


def create_player_database(name: str) -> Optional[Player]:
    """Adds a new player to the database

    Args:
        name (str): The players name from the form

    Returns:
        Optional[Player]: The player object from the database
    """
    if not name.strip():
        flash("Player name cannot be empty.", 'warning')
        return None

    new_player = Player(name=name)
    db.session.add(new_player)
    try:
        db.session.commit()
        return new_player
    except Exception as e:
        db.session.rollback()
        flash(f"Error creating player: {e}", 'danger')
        return None

    from typing import List


def get_players_by_game_id(game_id: int) -> List[Player]:
    """
    Retrieve all players participating in a specific game by the game ID.

    Args:
        game_id (int): The ID of the game to retrieve players from.

    Returns:
        List[Player]: A list of Player objects that are associated with the specified game.
    """
    players = Player.query.filter(Player.game_id == game_id).all()
    return players


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
        if player.game_id == game.id:
            print("Player is already in this game.")
            return False

        player.game_id = game.id
        players_in_game = get_players_by_game_id(game_id)
        if len(players_in_game) <= 1:
            player.is_game_owner = True
        else:
            player.is_game_owner = False
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while adding player to game: {e}")
        return False


def get_game_id_by_player_id(player_id: int) -> int:
    """
    Retrieves the game ID for a given player ID.

    Args:
        player_id (int): The ID of the player whose game ID is to be retrieved.

    Returns:
        int: The ID of the game associated with the player, or None if no game is associated or the player does not exist.
    """
    player = Player.query.get(player_id)
    if player and player.game_id:
        return player.game_id
    return None

# from datetime import datetime, timezone, timedelta
# def update_player_activity(player_id: int):
#    """Resets the players activity to the current
#
#    Args:
#        player_id (int): The id of the player
#    """
#    player = Player.query.filter_by(id=player_id).first()
#    if player:
#        player.last_active = datetime.now(timezone.utc)
#    else:
#        player = Player(id=player_id)
#        db.session.add(player)
#    db.session.commit()
#
#
# def remove_inactive_players(timeout: timedelta):
#    """Removes all inactive or disconnected players
#
#    Args:
#        timeout (timedelta): The timeout duration
#    """
#    timeout_threshold = datetime.now(timezone.utc) - timeout
#    inactive_players = Player.query.filter(
#        Player.last_active < timeout_threshold).all()
#    for player in inactive_players:
#        db.session.delete(player)
#    db.session.commit()
#
#
# def remove_inactive_players_from_game(timeout: timedelta):
#    """
#    Removes players from games who have been inactive longer than the specified timeout.
#
#    Args:
#        timeout (timedelta): The duration of time after which players are considered inactive.
#    """
#    now = datetime.now(timezone.utc)
#    timeout_threshold = now - timeout
#    inactive_players = Player.query.filter(
#        Player.last_active < timeout_threshold).all()
#    for player in inactive_players:
#        for game in player.games:
#            game.players.remove(player)
#        db.session.commit()
#


def remove_game(game_id: int):
    """Removes a specific game

    Args:
        game_id (int): The game to be removed
    """
    try:
        game = Game.query.get(game_id)
        if not game:
            print("Player not found.")
            return False
        db.session.delete(game)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while removing the player: {e}")
        return False


def remove_empty_game(game_id: int):
    """Removes the game if there are no players in it

    Args:
        game_id (int): The game to test
    """
    if len(get_players_by_game_id(game_id)) <= 0:
        remove_game(game_id)


def select_new_owner(game_id: int) -> bool:
    """
    Selects a new owner for the game from the remaining players.

    Args:
        game_id (int): The ID of the game.

    Returns:
        bool: True if a new owner was successfully selected, False otherwise.
    """
    remaining_players = Player.query.filter_by(
        game_id=game_id).order_by(Player.last_active).all()
    if remaining_players:
        print("new", new_owner.game_id, new_owner.is_game_owner)
        new_owner = remaining_players[0]
        new_owner.is_game_owner = True
        print("new", new_owner.game_id, new_owner.is_game_owner)
        db.session.commit()
        return True
    return False


def remove_player(player_id: int) -> bool:
    """
    Removes a player and all associated data from the database.

    Args:
        player_id (int): The ID of the player to remove.

    Returns:
        bool: True if the removal was successful, False otherwise.
    """
    try:
        player = Player.query.get(player_id)
        if not player:
            print("Player not found.")
            return False
        db.session.delete(player)
        db.session.commit()
        remove_empty_game(player.game_id)
        if check_owner(player.game_id, player):
            select_new_owner(player.game_id)
        return True
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while removing the player: {e}")
        return False


def update_settings(game_id: int, settings: dict):
    """
    Update game settings based on provided settings dictionary.

    Args:
        game_id (int): The ID of the game to update.
        settings (dict): A dictionary containing setting keys and their new values.
    """
    game = Game.query.get(game_id)
    if not game:
        return False, "Game not found"

    game.settings_starting_card_amount = settings.get(
        'starting_card_amount', game.settings_starting_card_amount)
    game.settings_black_card_finish = settings.get(
        'black_card_finish', game.settings_black_card_finish)
    game.settings_black_on_black = settings.get(
        'black_on_black', game.settings_black_on_black)
    game.settings_plus_two_stacking = settings.get(
        'plus_two_stacking', game.settings_plus_two_stacking)

    db.session.commit()
    return True, "Settings updated successfully"


def get_settings_by_game_id(game_id: int):
    """
    Retrieve settings for a specific game by game ID.

    Args:
        game_id (int): The ID of the game whose settings are to be retrieved.

    Returns:
        dict: A dictionary of settings if the game exists, otherwise None.
    """
    game = Game.query.get(game_id)
    if not game:
        return None

    settings = {
        "starting_card_amount": game.settings_starting_card_amount,
        "black_card_finish": game.settings_black_card_finish,
        "black_on_black": game.settings_black_on_black,
        "plus_two_stacking": game.settings_plus_two_stacking
    }
    return settings


def check_game_join(game_id: int) -> bool:
    """Checks if the game is joinable or ingame

    Args:
        game_id (int): The game id of the game

    Returns:
        bool: If the game is joinable
    """
    game = Game.query.get(game_id)
    return game.joinable


def start_game(game_id: int) -> bool:
    """Starts the game by setting it to unjoinable.

    Args:
        game_id (int): The id of the game to be started.

    Returns:
        bool: True if the game was successfully updated, False otherwise.
    """
    try:
        game = Game.query.get(game_id)
        if game and game.joinable:
            game.joinable = False
            db.session.commit()
            print(f"Game {game_id} started. It is now unjoinable.")
            return True
        elif game and not game.joinable:
            print(f"Game {game_id} was already started.")
            return False
        else:
            print("Game not found.")
            return False
    except Exception as e:
        db.session.rollback()
        print(f"Failed to start game {game_id}: {e}")
        return False


def game_has_password(game_id: int) -> bool:
    """Checks if the game has a password

    Args:
        game_id (int): The game id of the game

    Returns:
        bool: If the game has a password
    """
    game = Game.query.get(game_id)
    return not game.password_hash is None


def check_game_password(game_id: int, password: str) -> bool:
    """
    Checks if the provided password matches the hashed password of the game.

    Args:
        game_id (int): The ID of the game.
        password (str): The password to check.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    game = Game.query.get(game_id)
    if game and game.password_hash:
        return check_password_hash(game.password_hash, password)
    return False


def check_owner(game_id: int, player: Player) -> bool:
    """
    Checks if the given player is the owner of the specified game.

    Args:
        game_id (int): The ID of the game.
        player_id (int): The ID of the player.

    Returns:
        bool: True if the player is the owner, False otherwise.
    """
    if player and player.game_id == game_id and player.is_game_owner:
        return True
    return False


def check_game(game_id: int) -> bool:
    """
    Checks if the game exists.

    Args:
        game_id (int): The ID of the game to check.

    Returns:
        bool: True if the game exists, False otherwise.
    """
    game = Game.query.get(game_id)
    return game is not None


def check_player_in_game(player: Player) -> bool:
    """Check if the player is in a game

    Args:
        game_id (int): The game_id to check for
        player (Player): The player that could be in the game

    Returns:
        bool: If the player is in the game
    """
    return not player.game_id is None
