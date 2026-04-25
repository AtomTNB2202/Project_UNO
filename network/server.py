"""
Server

TODO:
Host-authoritative server.
This file receives client messages, validates them, updates game state,
and broadcasts synchronized results.
"""


class Server:
    def __init__(self, host="0.0.0.0", port=5000):
        # TODO: Store host
        # TODO: Store port
        # TODO: Initialize socket/server object
        # TODO: Initialize RoomManager
        # TODO: Initialize SyncManager
        pass

    def start(self):
        # TODO: Start server
        # TODO: Listen for client connections
        pass

    def handle_client_connection(self, connection, address):
        # TODO: Handle new client connection
        # TODO: Receive messages in loop
        # TODO: Decode message
        # TODO: Route message by message type
        # TODO: Handle disconnect
        pass

    def handle_message(self, connection, message):
        # TODO: Validate message
        # TODO: Get message type
        # TODO: Dispatch to correct handler
        pass

    def handle_create_room(self, connection, data):
        # TODO: Get host_id and host_name from data
        # TODO: Create room
        # TODO: Send room code back to host
        pass

    def handle_join_room(self, connection, data):
        # TODO: Get room_code, player_id, player_name
        # TODO: Join room
        # TODO: Broadcast updated player list
        pass

    def handle_leave_room(self, connection, data):
        # TODO: Get room_code and player_id
        # TODO: Remove player from room
        # TODO: Broadcast updated player list
        pass

    def handle_start_game(self, connection, data):
        # TODO: Validate player is host
        # TODO: Validate room can start
        # TODO: Start game
        # TODO: Broadcast game started
        pass

    def handle_play_card(self, connection, data):
        # TODO: Get room_code, player_id, card_index
        # TODO: Get optional chosen_color, zero_direction, seven_target_id
        # TODO: Call room.game_state.play_card(...)
        # TODO: Broadcast updated game state
        # TODO: If game ended, broadcast game ended
        pass

    def handle_draw_card(self, connection, data):
        # TODO: Get room_code and player_id
        # TODO: Call room.game_state.draw_card(...)
        # TODO: Broadcast updated game state
        pass

    def handle_choose_color(self, connection, data):
        # TODO: Handle color selection if your design separates it from play_card
        pass

    def handle_submit_reaction(self, connection, data):
        # TODO: Get room_code and player_id
        # TODO: Submit reaction for Rule 8
        # TODO: Broadcast reaction state/result if needed
        pass

    def handle_disconnect(self, connection):
        # TODO: Find player by connection
        # TODO: Remove player if game not started
        # TODO: Notify room if needed
        pass