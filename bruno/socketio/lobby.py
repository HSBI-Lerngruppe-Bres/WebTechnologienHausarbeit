from flask_socketio import join_room, leave_room, emit, Namespace
from flask_login import current_user, logout_user
from flask import current_app
from hashids import Hashids
from bruno.database.interaction.game import get_players_by_game_id, remove_player, player_join_game, get_game_id_by_player_id, update_settings, get_settings_by_game_id


class GameLobbyNamespace(Namespace):
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

    def on_join(self, data):
        """Handles player joining a game."""
        hashed_game_id = data['hashed_game_id']
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        # TODO Check if allowed
        # TODO Check if already in game SMEWHAT DONE
        game_id = hashids.decode(hashed_game_id)[0]
        join_room(hashed_game_id)
        player_join_game(current_user.id, game_id)
        self.send_update_player(game_id, hashed_game_id)
        self.send_update_settings(game_id, hashed_game_id)

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

    def on_update_settings(self, data):
        """Handles the settings update event
        """
        # TODO check if player permittet (OWNER)
        hashed_game_id = data['hashed_game_id']
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        game_id = hashids.decode(hashed_game_id)[0]
        update_settings(game_id, data["settings"])
        # TODO CHeck if numbers inbounds
        self.send_update_settings(game_id, hashed_game_id)

    def on_start_game(self, data):
        """When a player starts the game
        """
        print("STarting", data)
        # TODO Check player count
        hashed_game_id = data['hashed_game_id']
        emit("start_game", {"start": True}, room=hashed_game_id)
