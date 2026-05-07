"""
Server

Host-authoritative server.
This file receives client messages, validates them, updates game state,
and broadcasts synchronized results.
"""

from __future__ import annotations

import inspect
import socket
import threading
import uuid
from typing import Any, Callable, Optional

try:
    from .protocol import MessageType, Protocol
    from .room_manager import RoomManager
    from .sync_manager import SyncManager
except ImportError:
    from protocol import MessageType, Protocol
    from room_manager import RoomManager
    from sync_manager import SyncManager


class Server:
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 5000,
        game_state_factory: Optional[Callable[..., Any]] = None,
    ):
        # Store host and port
        self.host = host
        self.port = port

        # Initialize socket/server object
        self.server_socket: Optional[socket.socket] = None
        self.running = False

        # Initialize RoomManager and SyncManager
        self.room_manager = RoomManager()
        self.sync_manager = SyncManager(self)

        # Optional hook to connect this network layer to your UNO GameState class.
        self.game_state_factory = game_state_factory

        # Fast lookup tables for disconnect handling.
        self.connection_to_player: dict[socket.socket, str] = {}
        self.player_to_connection: dict[str, socket.socket] = {}

    def start(self):
        """Start server and listen for client connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.running = True

        print(f"Project UNO server listening on {self.host}:{self.port}")

        try:
            while self.running:
                connection, address = self.server_socket.accept()
                thread = threading.Thread(
                    target=self.handle_client_connection,
                    args=(connection, address),
                    daemon=True,
                )
                thread.start()
        finally:
            self.stop()

    def stop(self):
        """Stop the server socket."""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except OSError:
                pass
            self.server_socket = None

    def handle_client_connection(self, connection, address):
        """Receive, decode, and route messages from one client."""
        print(f"Client connected: {address}")
        recv_buffer = b""

        try:
            while self.running:
                chunk = connection.recv(4096)
                if not chunk:
                    break

                recv_buffer += chunk
                while Protocol.MESSAGE_DELIMITER in recv_buffer:
                    raw_message, recv_buffer = recv_buffer.split(
                        Protocol.MESSAGE_DELIMITER,
                        1,
                    )
                    if not raw_message.strip():
                        continue
                    try:
                        message = Protocol.decode(raw_message)
                        self.handle_message(connection, message)
                    except Exception as exc:
                        self.sync_manager.send_to_player(
                            connection,
                            Protocol.create_error(str(exc)),
                        )
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            pass
        finally:
            self.handle_disconnect(connection)
            try:
                connection.close()
            except OSError:
                pass
            print(f"Client disconnected: {address}")

    def handle_message(self, connection, message: dict):
        """Validate message and dispatch to correct handler."""
        if not Protocol.validate_message(message):
            self.sync_manager.send_to_player(
                connection,
                Protocol.create_error("Invalid message format"),
            )
            return

        message_type = message["type"]
        data = message.get("data", {})

        handlers = {
            MessageType.CREATE_ROOM: self.handle_create_room,
            MessageType.JOIN_ROOM: self.handle_join_room,
            MessageType.LEAVE_ROOM: self.handle_leave_room,
            MessageType.START_GAME: self.handle_start_game,
            MessageType.PLAY_CARD: self.handle_play_card,
            MessageType.DRAW_CARD: self.handle_draw_card,
            MessageType.CHOOSE_COLOR: self.handle_choose_color,
            MessageType.SUBMIT_REACTION: self.handle_submit_reaction,
        }

        handler = handlers.get(message_type)
        if not handler:
            self.sync_manager.send_to_player(
                connection,
                Protocol.create_error(f"Unsupported message type: {message_type}"),
            )
            return

        try:
            handler(connection, data)
        except Exception as exc:
            self.sync_manager.send_to_player(connection, Protocol.create_error(str(exc)))

    def handle_create_room(self, connection, data: dict):
        """Create room and send room code back to host."""
        host_id = data.get("player_id") or str(uuid.uuid4())
        host_name = data.get("player_name") or "Host"

        room = self.room_manager.create_room(host_id, host_name, connection)
        self._bind_connection(connection, host_id)

        self.sync_manager.send_to_player(
            connection,
            Protocol.create_message(
                MessageType.ROOM_CREATED,
                {
                    "room_code": room.room_code,
                    "player_id": host_id,
                    "host_id": room.host_id,
                },
            ),
        )
        self.sync_manager.broadcast_player_list(room)

    def handle_join_room(self, connection, data: dict):
        """Join room and broadcast updated player list."""
        room_code = self._require(data, "room_code").upper()
        player_id = data.get("player_id") or str(uuid.uuid4())
        player_name = data.get("player_name") or "Player"

        room = self.room_manager.join_room(room_code, player_id, player_name, connection)
        self._bind_connection(connection, player_id)

        self.sync_manager.send_to_player(
            connection,
            Protocol.create_message(
                MessageType.ROOM_JOINED,
                {
                    "room_code": room.room_code,
                    "player_id": player_id,
                    "host_id": room.host_id,
                },
            ),
        )
        self.sync_manager.broadcast_player_list(room)

    def handle_leave_room(self, connection, data: dict):
        """Remove player from room and broadcast updated player list."""
        room_code = self._require(data, "room_code").upper()
        player_id = self._get_player_id(connection, data)

        room = self.room_manager.leave_room(room_code, player_id)
        self._unbind_connection(connection, player_id)

        if room:
            self.sync_manager.broadcast_player_list(room)

    def handle_start_game(self, connection, data: dict):
        """Validate host/start conditions, start game, and broadcast state."""
        room = self._get_room_from_data(data)
        player_id = self._get_player_id(connection, data)

        if not room.is_host(player_id):
            self.sync_manager.broadcast_invalid_action(connection, "Only the host can start the game")
            return
        if not room.can_start():
            self.sync_manager.broadcast_invalid_action(
                connection,
                "Game requires 2 to 4 players",
            )
            return

        game_ended = (
            room.game_state is not None
            and (
                getattr(room.game_state, "winner", None) is not None
                or getattr(room.game_state, "winner_id", None) is not None
            )
        )

        if room.game_started and not game_ended:
            self.sync_manager.broadcast_invalid_action(connection, "Game has already started")
            return

        if room.game_state is None or game_ended:
            room.game_state = self._create_game_state(room)

        # Optional hook if your GameState has a start_game/start method.
        if room.game_state and hasattr(room.game_state, "start_game"):
            room.game_state.start_game()
        elif room.game_state and hasattr(room.game_state, "start"):
            room.game_state.start()

        room.game_started = True
        self.sync_manager.broadcast_game_started(room)

    def handle_play_card(self, connection, data: dict):
        """Call room.game_state.play_card(...) and broadcast updated state."""
        room = self._get_room_from_data(data)
        player_id = self._get_player_id(connection, data)
        card_index = self._require(data, "card_index")

        if not room.game_started or room.game_state is None:
            self.sync_manager.broadcast_invalid_action(connection, "Game has not started")
            return

        result = self._call_game_method(
            room.game_state,
            "play_card",
            player_id=player_id,
            card_index=card_index,
            chosen_color=data.get("chosen_color"),
            zero_direction=data.get("zero_direction"),
            seven_target_id=data.get("seven_target_id"),
        )

        self._broadcast_after_game_action(room, result)

    def handle_draw_card(self, connection, data: dict):
        """Call room.game_state.draw_card(...) and broadcast updated state."""
        room = self._get_room_from_data(data)
        player_id = self._get_player_id(connection, data)

        if not room.game_started or room.game_state is None:
            self.sync_manager.broadcast_invalid_action(connection, "Game has not started")
            return

        result = self._call_game_method(
            room.game_state,
            "draw_card",
            player_id=player_id,
        )
        self._broadcast_after_game_action(room, result)

    def handle_choose_color(self, connection, data: dict):
        """Handle color selection if your design separates it from play_card."""
        room = self._get_room_from_data(data)
        player_id = self._get_player_id(connection, data)
        chosen_color = self._require(data, "chosen_color")

        if not room.game_started or room.game_state is None:
            self.sync_manager.broadcast_invalid_action(connection, "Game has not started")
            return

        result = self._call_game_method(
            room.game_state,
            "choose_color",
            player_id=player_id,
            chosen_color=chosen_color,
        )
        self._broadcast_after_game_action(room, result)

    def handle_submit_reaction(self, connection, data: dict):
        """Submit reaction for Rule 8 and broadcast reaction result/state."""
        room = self._get_room_from_data(data)
        player_id = self._get_player_id(connection, data)

        if not room.game_started or room.game_state is None:
            self.sync_manager.broadcast_invalid_action(connection, "Game has not started")
            return

        result = self._call_game_method(
            room.game_state,
            "submit_reaction",
            player_id=player_id,
        )

        if isinstance(result, dict) and result.get("reaction_result"):
            self.sync_manager.broadcast_reaction_result(room, result["reaction_result"])

        self._broadcast_after_game_action(room, result)

    def handle_disconnect(self, connection):
        """Find player by connection, remove before game or mark disconnected in-game."""
        room, player_id = self.room_manager.find_room_by_connection(connection)
        if not room or not player_id:
            return

        if room.game_started:
            room.mark_disconnected(player_id)
            self.sync_manager.broadcast_player_list(room)
            self.sync_manager.broadcast_game_state(room)
        else:
            remaining_room = self.room_manager.leave_room(room.room_code, player_id)
            if remaining_room:
                self.sync_manager.broadcast_player_list(remaining_room)

        self._unbind_connection(connection, player_id)

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    def _bind_connection(self, connection, player_id: str):
        self.connection_to_player[connection] = player_id
        self.player_to_connection[player_id] = connection

    def _unbind_connection(self, connection, player_id: Optional[str] = None):
        player_id = player_id or self.connection_to_player.get(connection)
        self.connection_to_player.pop(connection, None)
        if player_id:
            self.player_to_connection.pop(player_id, None)

    def _get_player_id(self, connection, data: dict) -> str:
        player_id = data.get("player_id") or self.connection_to_player.get(connection)
        if not player_id:
            raise ValueError("Missing player_id")
        return player_id

    def _get_room_from_data(self, data: dict):
        room_code = self._require(data, "room_code").upper()
        room = self.room_manager.get_room(room_code)
        if not room:
            raise ValueError("Room not found")
        return room

    @staticmethod
    def _require(data: dict, key: str):
        value = data.get(key)
        if value is None or value == "":
            raise ValueError(f"Missing required field: {key}")
        return value

    def _create_game_state(self, room):
        """Create GameState using a provided factory or simple dynamic import.

        This keeps the network layer independent from your game-core branch.
        Pass game_state_factory=YourGameState when constructing Server if needed.
        """
        factory = self.game_state_factory

        if factory is None:
            try:
                from game_state import GameState  # type: ignore

                factory = GameState
            except Exception:
                return None

        players = room.get_player_list()
        player_ids = room.get_player_ids()

        # Try common constructor shapes.
        for args in ((player_ids,), (players,), (room,), ()):  # noqa: B007
            try:
                return factory(*args)
            except TypeError:
                continue

        # If all signatures fail, surface the original problem clearly.
        raise ValueError("Could not construct GameState with known constructor signatures")

    def _call_game_method(self, game_state, method_name: str, **kwargs):
        method = getattr(game_state, method_name, None)
        if not method:
            raise ValueError(f"GameState does not implement {method_name}()")

        # Remove None values so optional network fields do not break strict signatures.
        kwargs = {key: value for key, value in kwargs.items() if value is not None}

        # Prefer keyword arguments if the GameState method supports them.
        try:
            signature = inspect.signature(method)
            accepted_kwargs = {
                key: value
                for key, value in kwargs.items()
                if key in signature.parameters
            }
            return method(**accepted_kwargs)
        except TypeError:
            pass

        # Fallbacks for common positional signatures.
        player_id = kwargs.get("player_id")
        card_index = kwargs.get("card_index")
        chosen_color = kwargs.get("chosen_color")
        zero_direction = kwargs.get("zero_direction")
        seven_target_id = kwargs.get("seven_target_id")

        if method_name == "play_card":
            return method(player_id, card_index, chosen_color, zero_direction, seven_target_id)
        if player_id is not None:
            return method(player_id)
        return method()

    def _broadcast_after_game_action(self, room, result):
        """Broadcast state, reaction events, and game end when applicable."""
        if isinstance(result, dict):
            if result.get("reaction_started"):
                self.sync_manager.broadcast_reaction_started(room, result["reaction_started"])
            if result.get("reaction_result"):
                self.sync_manager.broadcast_reaction_result(room, result["reaction_result"])

        self.sync_manager.broadcast_game_state(room)

        winner_id = self._extract_winner_id(room.game_state, result)
        if winner_id:
            self.sync_manager.broadcast_game_ended(room, winner_id)

    @staticmethod
    def _extract_winner_id(game_state, result) -> Optional[str]:
        if isinstance(result, dict):
            if result.get("winner_id"):
                return result["winner_id"]
            if result.get("game_ended") and result.get("winner"):
                return result["winner"]

        for attr in ("winner_id", "winner"):
            value = getattr(game_state, attr, None)
            if value:
                return value

        for attr in ("is_game_over", "game_over"):
            value = getattr(game_state, attr, None)
            if callable(value) and value():
                return getattr(game_state, "winner_id", None) or getattr(game_state, "winner", None)
            if isinstance(value, bool) and value:
                return getattr(game_state, "winner_id", None) or getattr(game_state, "winner", None)

        return None


if __name__ == "__main__":
    Server().start()
