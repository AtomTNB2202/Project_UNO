"""
Room Manager

Manages room creation, joining, leaving, and room lookup.
"""

from __future__ import annotations

import random
import string
import threading
from typing import Any, Dict, List, Optional


class Room:
    MAX_PLAYERS = 4
    MIN_PLAYERS_TO_START = 2

    def __init__(self, room_code: str, host_id: str):
        # Store room code and host id
        self.room_code = room_code.upper()
        self.host_id = host_id

        # Store connected players:
        # player_id -> {id, name, connection, is_host, connected}
        self.players: Dict[str, Dict[str, Any]] = {}

        # Store game state and whether game has started
        self.game_state: Any = None
        self.game_started = False

        self.lock = threading.RLock()

    def add_player(self, player_id: str, player_name: str, connection=None):
        """Validate and add player to room."""
        with self.lock:
            if self.game_started:
                raise ValueError("Game has already started")
            if player_id in self.players:
                raise ValueError("Player is already in this room")
            if len(self.players) >= self.MAX_PLAYERS:
                raise ValueError("Room is full")

            self.players[player_id] = {
                "id": player_id,
                "name": player_name,
                "connection": connection,
                "is_host": player_id == self.host_id,
                "connected": True,
            }

            # Optional hook for a future GameState implementation.
            if self.game_state and hasattr(self.game_state, "add_player"):
                self.game_state.add_player(player_id, player_name)

    def remove_player(self, player_id: str):
        with self.lock:
            if player_id not in self.players:
                return

            if self.game_started:
                self.players[player_id]["connected"] = False
                self.players[player_id]["connection"] = None
                return

            del self.players[player_id]

            if self.host_id == player_id:
                remaining_players = list(self.players.keys())
                self.host_id = remaining_players[0] if remaining_players else None

    def mark_disconnected(self, player_id: str):
        """Keep the player in the room but mark the socket as disconnected."""
        with self.lock:
            if player_id in self.players:
                self.players[player_id]["connection"] = None
                self.players[player_id]["connected"] = False

    def is_host(self, player_id: str) -> bool:
        """Return True if player_id is host."""
        return player_id == self.host_id

    def can_start(self) -> bool:
        """Return True if room has 2-4 players."""
        return self.MIN_PLAYERS_TO_START <= len(self.players) <= self.MAX_PLAYERS

    def get_player_ids(self) -> List[str]:
        """Return list of player ids."""
        return list(self.players.keys())

    def get_connection(self, player_id: str):
        """Return connection object for player."""
        player = self.players.get(player_id)
        return player.get("connection") if player else None

    def get_player_list(self) -> List[dict]:
        """Return public room player data safe to broadcast."""
        return [
            {
                "id": player["id"],
                "name": player["name"],
                "is_host": player["id"] == self.host_id,
                "connected": bool(player.get("connected", True)),
            }
            for player in self.players.values()
        ]

    def is_empty(self) -> bool:
        return len(self.players) == 0

    def find_player_by_connection(self, connection) -> Optional[str]:
        for player_id, player in self.players.items():
            if player.get("connection") is connection:
                return player_id
        return None


class RoomManager:
    def __init__(self):
        # Store all rooms by room code
        self.rooms: Dict[str, Room] = {}
        self.lock = threading.RLock()

    def generate_room_code(self) -> str:
        """Generate unique 4-character room code."""
        alphabet = string.ascii_uppercase + string.digits
        with self.lock:
            while True:
                room_code = "".join(random.choices(alphabet, k=4))
                if room_code not in self.rooms:
                    return room_code

    def create_room(self, host_id: str, host_name: str, connection=None) -> Room:
        """Create a room and add the host player."""
        with self.lock:
            room_code = self.generate_room_code()
            room = Room(room_code, host_id)
            room.add_player(host_id, host_name, connection)
            self.rooms[room_code] = room
            return room

    def join_room(self, room_code: str, player_id: str, player_name: str, connection=None) -> Room:
        """Find room, add player, and return room."""
        room_code = room_code.upper()
        with self.lock:
            room = self.rooms.get(room_code)
            if not room:
                raise ValueError("Room not found")
            room.add_player(player_id, player_name, connection)
            return room

    def leave_room(self, room_code: str, player_id: str) -> Optional[Room]:
        """Remove player and delete room if empty.

        Returns the room if it still exists after the player leaves,
        otherwise returns None.
        """
        room_code = room_code.upper()
        with self.lock:
            room = self.rooms.get(room_code)
            if not room:
                return None
            room.remove_player(player_id)
            if room.is_empty():
                del self.rooms[room_code]
                return None
            return room

    def get_room(self, room_code: str) -> Optional[Room]:
        """Return room by room code."""
        return self.rooms.get(room_code.upper())

    def find_room_by_player(self, player_id: str) -> Optional[Room]:
        """Find room containing player_id."""
        for room in self.rooms.values():
            if player_id in room.players:
                return room
        return None

    def find_room_by_connection(self, connection) -> tuple[Optional[Room], Optional[str]]:
        """Find room and player_id by socket connection."""
        for room in self.rooms.values():
            player_id = room.find_player_by_connection(connection)
            if player_id:
                return room, player_id
        return None, None
