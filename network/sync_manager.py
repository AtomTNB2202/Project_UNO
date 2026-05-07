"""
Sync Manager

Broadcasts game state and room state to all clients.
"""

from __future__ import annotations

try:
    from .protocol import MessageType, Protocol
except ImportError:
    from protocol import MessageType, Protocol


class SyncManager:
    def __init__(self, server=None):
        # Store server/socket reference if needed
        self.server = server

    def send_to_player(self, player_connection, message: dict) -> bool:
        """Send one message to one player."""
        if player_connection is None:
            return False
        try:
            player_connection.sendall(Protocol.encode(message))
            return True
        except OSError:
            return False

    def broadcast_to_room(self, room, message: dict):
        """Send message to every connected player in room."""
        for player_id in room.get_player_ids():
            self.send_to_player(room.get_connection(player_id), message)

    def broadcast_player_list(self, room):
        """Build player list data and broadcast it to room."""
        message = Protocol.create_message(
            MessageType.PLAYER_LIST_UPDATED,
            {
                "room_code": room.room_code,
                "host_id": room.host_id,
                "players": room.get_player_list(),
            },
        )
        self.broadcast_to_room(room, message)

    def broadcast_game_state(self, room):
        """Send private game state to each player.

        If GameState implements to_dict_for_player(player_id), each player receives
        only their own private hand/state. Otherwise, a safe room-level fallback is sent.
        """
        for player_id in room.get_player_ids():
            state = self._build_state_for_player(room, player_id)
            message = Protocol.create_message(
                MessageType.STATE_UPDATED,
                {
                    "room_code": room.room_code,
                    "player_id": player_id,
                    "state": state,
                },
            )
            self.send_to_player(room.get_connection(player_id), message)

    def broadcast_invalid_action(self, player_connection, reason: str):
        """Send invalid action message to one player."""
        self.send_to_player(
            player_connection,
            Protocol.create_message(
                MessageType.INVALID_ACTION,
                {"reason": str(reason)},
            ),
        )

    def broadcast_game_started(self, room):
        """Notify all players that game started and broadcast initial game state."""
        self.broadcast_to_room(
            room,
            Protocol.create_message(
                MessageType.GAME_STARTED,
                {
                    "room_code": room.room_code,
                    "players": room.get_player_list(),
                },
            ),
        )
        self.broadcast_game_state(room)

    def broadcast_game_ended(self, room, winner_id: str):
        """Notify all players that game ended."""
        self.broadcast_to_room(
            room,
            Protocol.create_message(
                MessageType.GAME_ENDED,
                {
                    "room_code": room.room_code,
                    "winner_id": winner_id,
                },
            ),
        )

    def broadcast_reaction_started(self, room, event_data: dict):
        """Notify all players that Rule 8 reaction event started."""
        self.broadcast_to_room(
            room,
            Protocol.create_message(MessageType.REACTION_STARTED, event_data or {}),
        )

    def broadcast_reaction_result(self, room, result_data: dict):
        """Notify all players about Rule 8 result."""
        self.broadcast_to_room(
            room,
            Protocol.create_message(MessageType.REACTION_RESULT, result_data or {}),
        )

    def _build_state_for_player(self, room, player_id: str) -> dict:
        game_state = getattr(room, "game_state", None)
        if game_state and hasattr(game_state, "to_dict_for_player"):
            return game_state.to_dict_for_player(player_id)
        if game_state and hasattr(game_state, "to_dict"):
            return game_state.to_dict()

        return {
            "room_code": room.room_code,
            "host_id": room.host_id,
            "game_started": room.game_started,
            "players": room.get_player_list(),
            "note": "No GameState object is attached yet.",
        }
