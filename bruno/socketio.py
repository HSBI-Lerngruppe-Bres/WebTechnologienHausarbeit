from flask_socketio import join_room, leave_room, emit, Namespace
from flask_login import current_user, logout_user
from functools import wraps
from flask import current_app
from hashids import Hashids
from bruno.database.interaction import get_players_by_game_id, check_owner, remove_player, player_join_game, get_game_id_by_player_id, update_settings, get_settings_by_game_id, check_game_join, start_game


def authenticated_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            emit('kick', {
                 'message': 'User not authenticated'}, namespace='/game')
            return
        return f(*args, **kwargs)
    return wrapped


class GameNamespace(Namespace):
    @staticmethod
    def send_update_player(game_id: int, hashed_game_id: str):
        """Emits an update for all players

        Args:
            game_id (int): The id of the game
            hashed_game_id (str): The hashed game id
        """
        players = get_players_by_game_id(game_id)
        players_data = [{'name': player.name, 'id': player.id}
                        for player in players]
        emit('update_players', {'players': players_data},
             room=hashed_game_id)

    @staticmethod
    def send_update_settings(game_id: int, hashed_game_id: str):
        """Emits an update for all players to the new settings

        Args:
            game_id (int): The id of the game
            hashed_game_id (str): The hashed game id
        """
        settings_data = get_settings_by_game_id(game_id)
        emit('update_settings', {'settings': settings_data},
             room=hashed_game_id)

    @staticmethod
    def check_settings(settings: dict):
        if int(settings.get("starting_card_amount")) > 20 or 2 > int(settings.get("starting_card_amount")):
            return False
        return True

    @authenticated_only
    def on_join(self, data):
        """Handles player joining a game."""
        hashed_game_id = data['hashed_game_id']
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        # TODO Check if allowed nessasary?
        game_id = hashids.decode(hashed_game_id)[0]
        if not check_game_join(game_id):
            emit('kick', {'message': 'Game already started'},
                 namespace='/lobby')
            return
        join_room(hashed_game_id)
        player_join_game(current_user.id, game_id)
        self.send_update_player(game_id, hashed_game_id)
        self.send_update_settings(game_id, hashed_game_id)

    @authenticated_only
    def on_disconnect(self):
        """Handles player disconnection."""
        game_id = get_game_id_by_player_id(current_user.id)
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        hashed_game_id = hashids.encode(game_id)
        if game_id:
            remove_player(current_user.id)
            self.send_update_player(game_id, hashed_game_id)
            leave_room(hashed_game_id)
        logout_user()

    @authenticated_only
    def on_update_settings(self, data):
        """Handles the settings update event
        """
        hashed_game_id = data['hashed_game_id']
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        game_id = hashids.decode(hashed_game_id)[0]
        if self.check_settings(data["settings"]) and check_owner(game_id, current_user):
            update_settings(game_id, data["settings"])
        self.send_update_settings(game_id, hashed_game_id)

    @authenticated_only
    def on_start_game(self, data):
        """When a player starts the game
        """
        print("STarting", data)
        hashed_game_id = data['hashed_game_id']
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        game_id = hashids.decode(hashed_game_id)[0]
        if len(get_players_by_game_id(game_id)) < current_app.config.get("MIN_PLAYERS_PER_GAME") or not check_owner(game_id, current_user):
            emit("start_game", {"start": False}, room=hashed_game_id)
            return
        start_game(game_id)
        emit("start_game", {"start": True}, room=hashed_game_id)
