"""
Client

Client-side networking wrapper. UI should call this class instead of using
raw socket directly.
"""

from __future__ import annotations

import socket
import threading
import uuid
from typing import Callable, Dict, List, Optional

try:
    from .protocol import MessageType, Protocol
except ImportError:  # Allows running this file directly during simple tests.
    from protocol import MessageType, Protocol


Callback = Callable[[dict], None]


class Client:
    def __init__(self, server_host: str = "127.0.0.1", server_port: int = 5000):
        # Store server address
        self.server_host = server_host
        self.server_port = server_port

        # Initialize socket/client object
        self.socket: Optional[socket.socket] = None
        self.connected = False
        self._recv_buffer = b""
        self._listen_thread: Optional[threading.Thread] = None

        # Store player id and current room code
        self.player_id = str(uuid.uuid4())
        self.player_name: Optional[str] = None
        self.room_code: Optional[str] = None

        # Store callback handlers for UI: message_type -> callbacks
        self.callbacks: Dict[str, List[Callback]] = {}

    def connect(self) -> bool:
        """Connect to server and start the background listener thread."""
        if self.connected:
            return True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))
        self.connected = True

        self._listen_thread = threading.Thread(target=self.listen, daemon=True)
        self._listen_thread.start()
        return True

    def disconnect(self):
        """Disconnect from server."""
        if not self.connected:
            return

        try:
            if self.room_code:
                self.leave_room()
        except OSError:
            pass

        self.connected = False
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.socket.close()
            self.socket = None

    def listen(self):
        """Listen for newline-delimited JSON messages from the server."""
        while self.connected and self.socket:
            try:
                chunk = self.socket.recv(4096)
                if not chunk:
                    break

                self._recv_buffer += chunk
                while Protocol.MESSAGE_DELIMITER in self._recv_buffer:
                    raw_message, self._recv_buffer = self._recv_buffer.split(
                        Protocol.MESSAGE_DELIMITER,
                        1,
                    )
                    if not raw_message.strip():
                        continue
                    message = Protocol.decode(raw_message)
                    self.handle_server_message(message)
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                break
            except Exception as exc:
                self.handle_server_message(
                    Protocol.create_error(f"Client listen error: {exc}")
                )

        self.connected = False

    def send_message(self, message_type: str, data: Optional[dict] = None):
        """Create, encode, and send a message to the server."""
        if not self.connected or not self.socket:
            raise ConnectionError("Client is not connected to a server")

        message = Protocol.create_message(message_type, data or {})
        self.socket.sendall(Protocol.encode(message))

    def create_room(self, player_name: str):
        """Send CREATE_ROOM request."""
        self.player_name = player_name
        self.send_message(
            MessageType.CREATE_ROOM,
            {
                "player_id": self.player_id,
                "player_name": player_name,
            },
        )

    def join_room(self, room_code: str, player_name: str):
        """Send JOIN_ROOM request."""
        self.player_name = player_name
        self.room_code = room_code.upper()
        self.send_message(
            MessageType.JOIN_ROOM,
            {
                "room_code": self.room_code,
                "player_id": self.player_id,
                "player_name": player_name,
            },
        )

    def leave_room(self):
        """Send LEAVE_ROOM request."""
        if not self.room_code:
            return
        self.send_message(
            MessageType.LEAVE_ROOM,
            {
                "room_code": self.room_code,
                "player_id": self.player_id,
            },
        )
        self.room_code = None

    def start_game(self):
        """Send START_GAME request."""
        self._require_room()
        self.send_message(
            MessageType.START_GAME,
            {
                "room_code": self.room_code,
                "player_id": self.player_id,
            },
        )

    def play_card(
        self,
        card_index: int,
        chosen_color: Optional[str] = None,
        zero_direction: Optional[str] = None,
        seven_target_id: Optional[str] = None,
    ):
        """Send PLAY_CARD request."""
        self._require_room()
        data = {
            "room_code": self.room_code,
            "player_id": self.player_id,
            "card_index": card_index,
        }
        if chosen_color is not None:
            data["chosen_color"] = chosen_color
        if zero_direction is not None:
            data["zero_direction"] = zero_direction
        if seven_target_id is not None:
            data["seven_target_id"] = seven_target_id

        self.send_message(MessageType.PLAY_CARD, data)

    def draw_card(self):
        """Send DRAW_CARD request."""
        self._require_room()
        self.send_message(
            MessageType.DRAW_CARD,
            {
                "room_code": self.room_code,
                "player_id": self.player_id,
            },
        )

    def submit_reaction(self):
        """Send SUBMIT_REACTION request."""
        self._require_room()
        self.send_message(
            MessageType.SUBMIT_REACTION,
            {
                "room_code": self.room_code,
                "player_id": self.player_id,
            },
        )

    def on(self, message_type: str, callback: Callback):
        """Register callback for a message type.

        Use message_type="*" to receive every server message.
        """
        self.callbacks.setdefault(message_type, []).append(callback)

    def handle_server_message(self, message: dict):
        """Call registered callback based on message type."""
        message_type = message.get("type")
        data = message.get("data", {})

        # Keep basic client state in sync.
        if message_type in (MessageType.ROOM_CREATED, MessageType.ROOM_JOINED):
            self.room_code = data.get("room_code", self.room_code)
            self.player_id = data.get("player_id", self.player_id)

        for callback in self.callbacks.get(message_type, []):
            callback(message)
        for callback in self.callbacks.get("*", []):
            callback(message)

    def _require_room(self):
        if not self.room_code:
            raise ValueError("Client is not currently in a room")
