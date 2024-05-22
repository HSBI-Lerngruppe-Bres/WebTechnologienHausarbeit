from flask_socketio import join_room, leave_room, emit, Namespace
from flask_login import current_user, logout_user
from functools import wraps
from flask import current_app
from hashids import Hashids
from bruno.database.interaction import lower_uno_score, set_uno, player_won, check_for_win, remove_finished_status, randomize_order, handle_card_action, advance_turn, is_player_turn, set_new_last_card, get_last_card_by_game, check_card_playable, remove_card_from_player, remove_all_cards, get_cards_by_player, card_amounts_turn_in_game, draw_cards, select_start_card, get_players_by_game_id, check_owner, remove_player, player_join_game, get_game_id_by_player_id, update_settings, get_settings_by_game_id, check_game_join, start_game


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
        players = [{'name': player.name, 'id': player.id}
                   for player in players]
        emit('update_players', {'players': players},
             room=hashed_game_id)

    @staticmethod
    def send_update_settings(game_id: int, hashed_game_id: str):
        """Emits an update for all players to the new settings

        Args:
            game_id (int): The id of the game
            hashed_game_id (str): The hashed game id
        """
        settings = get_settings_by_game_id(game_id)
        emit('update_settings', {'settings': settings},
             room=hashed_game_id)

    @staticmethod
    def check_settings(settings: dict) -> bool:
        """Checks if the settings are valid

        Args:
            settings (dict): The settings dictionary

        Returns:
            bool: If the request is valid
        """
        if int(settings.get("starting_card_amount")) > 20 or 2 > int(settings.get("starting_card_amount")):
            return False
        return True

    @staticmethod
    def send_update_cards(game_id: int, hashed_game_id: str, pull_cards=False):
        """Sends the card amount of all players in a game

        Args:
            game_id (int): The games id
            hashed_game_id (str): The hashed game id
        """
        cards = card_amounts_turn_in_game(game_id)
        last_card = get_last_card_by_game(game_id)
        emit('update_cards', {'cards': cards, 'last_card': last_card, 'pull_cards': pull_cards},
             room=hashed_game_id)

    @authenticated_only
    def on_join(self, data):
        """Handles player joining a game."""
        hashed_game_id = data.get('hashed_game_id')
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        # TODO Check if allowed nessasary?
        game_id = hashids.decode(hashed_game_id)[0]
        if not check_game_join(game_id):
            emit('kick', {'message': 'Game already started'},
                 namespace='/game')
            return
        join_room(hashed_game_id)
        player_join_game(current_user.id, game_id)
        self.send_update_player(game_id, hashed_game_id)
        self.send_update_settings(game_id, hashed_game_id)

    @authenticated_only
    def on_rejoin(self, data):
        hashed_game_id = data.get('hashed_game_id')
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        # TODO Check if allowed nessasary?
        game_id = hashids.decode(hashed_game_id)[0]
        if not check_game_join(game_id):
            emit('kick', {'message': 'Game already started'},
                 namespace='/game')
            return
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
        hashed_game_id = data.get('hashed_game_id')
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        game_id = hashids.decode(hashed_game_id)[0]
        if self.check_settings(data.get("settings")) and check_owner(game_id, current_user):
            update_settings(game_id, data.get("settings"))
        self.send_update_settings(game_id, hashed_game_id)

    @authenticated_only
    def on_start_game(self, data):
        """When a player starts the game
        """
        hashed_game_id = data.get('hashed_game_id')
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        game_id = hashids.decode(hashed_game_id)[0]
        if len(get_players_by_game_id(game_id)) < current_app.config.get("MIN_PLAYERS_PER_GAME") or not check_owner(game_id, current_user):
            emit("start_game", {
                 "start": False, "message": "There are not enogth players."}, namespace='/game')
            return
        start_game(game_id)
        for player in get_players_by_game_id(game_id):
            remove_finished_status(player)
            remove_all_cards(player)
            draw_cards(player, get_settings_by_game_id(
                game_id)["starting_card_amount"])
        select_start_card(game_id)
        randomize_order(game_id)
        emit("start_game", {"start": True}, room=hashed_game_id)

    @authenticated_only
    def on_move(self, data):
        """When a users plays a move
        """
        hashed_game_id = data.get('hashed_game_id')
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        game_id = hashids.decode(hashed_game_id)[0]
        cards_data = get_cards_by_player(current_user)
        action = data.get('action')
        card_id = data.get('card_id')
        selected_color = data.get('selected_color')
        if not is_player_turn(game_id, current_user):
            return
        if action == 'card' and card_id and check_card_playable(card_id, game_id):
            if not handle_card_action(card_id, game_id, selected_color):
                return
            if not remove_card_from_player(current_user, card_id):
                return
            set_new_last_card(game_id, card_id)
            if check_for_win(current_user):
                player_won(current_user)
            else:
                lower_uno_score(current_user)
        elif action == 'card':
            return
        if action == 'draw':
            draw_cards(current_user, 1)
        if not advance_turn(game_id)[0]:
            emit('end_game', {'end': True},
                 room=hashed_game_id, namespace='/game')
            return
        emit("update_own_cards", {"cards": cards_data}, namespace='/game')
        self.send_update_cards(game_id, hashed_game_id, True)

    @authenticated_only
    def on_request_cards(self, data):
        """When the client requests to receive its cards
        """
        # TODO some logic
        hashed_game_id = data.get('hashed_game_id')
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        game_id = hashids.decode(hashed_game_id)[0]
        cards_data = get_cards_by_player(current_user)
        emit("update_own_cards", {"cards": cards_data}, namespace='/game')
        self.send_update_cards(game_id, hashed_game_id)

    @authenticated_only
    def on_uno(self, data):
        hashed_game_id = data.get('hashed_game_id')
        hashids = Hashids(salt=current_app.config['SECRET_KEY'], min_length=5)
        game_id = hashids.decode(hashed_game_id)[0]
        if not is_player_turn(game_id, current_user):
            return
        set_uno(current_user)
        emit("uno", {"player_name": current_user.name}, room=hashed_game_id)
