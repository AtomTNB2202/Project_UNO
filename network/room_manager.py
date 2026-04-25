"""
Room Manager

TODO:
Manage room creation, joining, leaving, and room lookup.
"""


class Room:
    def __init__(self, room_code, host_id):
        # TODO: Store room code
        # TODO: Store host id
        # TODO: Store connected players
        # TODO: Store game state
        # TODO: Store whether game has started
        pass

    def add_player(self, player_id, player_name, connection=None):
        # TODO: Validate room is not full
        # TODO: Validate game has not started
        # TODO: Add player to room
        # TODO: Add player to game state
        pass

    def remove_player(self, player_id):
        # TODO: Remove player from room
        # TODO: Remove player from game state if game has not started
        pass

    def is_host(self, player_id):
        # TODO: Return True if player_id is host
        pass

    def can_start(self):
        # TODO: Return True if room has 2-4 players
        pass

    def get_player_ids(self):
        # TODO: Return list of player ids
        pass

    def get_connection(self, player_id):
        # TODO: Return connection object for player
        pass


class RoomManager:
    def __init__(self):
        # TODO: Store all rooms by room code
        pass

    def generate_room_code(self):
        # TODO: Generate unique room code
        pass

    def create_room(self, host_id, host_name, connection=None):
        # TODO: Generate room code
        # TODO: Create Room object
        # TODO: Add host player
        # TODO: Store room
        # TODO: Return room
        pass

    def join_room(self, room_code, player_id, player_name, connection=None):
        # TODO: Find room by room code
        # TODO: Add player to room
        # TODO: Return room
        pass

    def leave_room(self, room_code, player_id):
        # TODO: Find room
        # TODO: Remove player
        # TODO: Delete room if empty
        pass

    def get_room(self, room_code):
        # TODO: Return room by room code
        pass

    def find_room_by_player(self, player_id):
        # TODO: Find room containing player_id
        pass