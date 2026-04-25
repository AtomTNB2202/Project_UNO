"""
Client

TODO:
Client-side networking wrapper.
UI should call this class instead of using raw socket directly.
"""


class Client:
    def __init__(self, server_host="127.0.0.1", server_port=5000):
        # TODO: Store server address
        # TODO: Initialize socket/client object
        # TODO: Store player id
        # TODO: Store room code
        # TODO: Store callback handlers for UI
        pass

    def connect(self):
        # TODO: Connect to server
        pass

    def disconnect(self):
        # TODO: Disconnect from server
        pass

    def listen(self):
        # TODO: Listen for messages from server
        # TODO: Decode message
        # TODO: Dispatch message to UI callbacks
        pass

    def send_message(self, message_type, data=None):
        # TODO: Create message using Protocol
        # TODO: Encode message
        # TODO: Send to server
        pass

    def create_room(self, player_name):
        # TODO: Send CREATE_ROOM request
        pass

    def join_room(self, room_code, player_name):
        # TODO: Send JOIN_ROOM request
        pass

    def leave_room(self):
        # TODO: Send LEAVE_ROOM request
        pass

    def start_game(self):
        # TODO: Send START_GAME request
        pass

    def play_card(
        self,
        card_index,
        chosen_color=None,
        zero_direction=None,
        seven_target_id=None,
    ):
        # TODO: Send PLAY_CARD request
        pass

    def draw_card(self):
        # TODO: Send DRAW_CARD request
        pass

    def submit_reaction(self):
        # TODO: Send SUBMIT_REACTION request
        pass

    def on(self, message_type, callback):
        # TODO: Register callback for message type
        pass

    def handle_server_message(self, message):
        # TODO: Call registered callback based on message type
        pass