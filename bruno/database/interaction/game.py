from typing import List
from ..models import Game, Player, db
from datetime import datetime, timezone, timedelta


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
        player.game_id = game.id  # Set the game ID directly in the player record
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

#
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
