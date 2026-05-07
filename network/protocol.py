"""
Network Protocol

Defines the message types and the JSON-over-TCP format used between
Project UNO clients and the host-authoritative server.

Transport format:
    one JSON message per line, encoded as UTF-8 bytes.

Example:
    {"type": "CREATE_ROOM", "data": {"player_id": "...", "player_name": "Alice"}}\n
The newline delimiter is important because TCP is a stream protocol: one recv()
call may contain half a message or multiple messages.
"""

from __future__ import annotations

import json
from typing import Any, Dict


class MessageType:
    # Room events: client -> server
    CREATE_ROOM = "CREATE_ROOM"
    JOIN_ROOM = "JOIN_ROOM"
    LEAVE_ROOM = "LEAVE_ROOM"
    START_GAME = "START_GAME"

    # Gameplay events: client -> server
    PLAY_CARD = "PLAY_CARD"
    DRAW_CARD = "DRAW_CARD"
    CHOOSE_COLOR = "CHOOSE_COLOR"
    CHOOSE_ZERO_DIRECTION = "CHOOSE_ZERO_DIRECTION"
    CHOOSE_SEVEN_TARGET = "CHOOSE_SEVEN_TARGET"
    SUBMIT_REACTION = "SUBMIT_REACTION"

    # Server response events: server -> client
    ROOM_CREATED = "ROOM_CREATED"
    ROOM_JOINED = "ROOM_JOINED"
    PLAYER_LIST_UPDATED = "PLAYER_LIST_UPDATED"
    GAME_STARTED = "GAME_STARTED"
    STATE_UPDATED = "STATE_UPDATED"
    INVALID_ACTION = "INVALID_ACTION"
    REACTION_STARTED = "REACTION_STARTED"
    REACTION_RESULT = "REACTION_RESULT"
    GAME_ENDED = "GAME_ENDED"
    ERROR = "ERROR"

    @classmethod
    def all(cls) -> set[str]:
        """Return all valid message type values."""
        return {
            value
            for name, value in vars(cls).items()
            if name.isupper() and isinstance(value, str)
        }


class Protocol:
    MESSAGE_DELIMITER = b"\n"

    @staticmethod
    def create_message(message_type: str, data: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Return the standard message dictionary."""
        return {
            "type": message_type,
            "data": data or {},
        }

    @staticmethod
    def validate_message(message: Dict[str, Any]) -> bool:
        """Check that a decoded message has the expected shape."""
        if not isinstance(message, dict):
            return False
        if "type" not in message:
            return False
        if "data" not in message:
            return False
        if message["type"] not in MessageType.all():
            return False
        if not isinstance(message["data"], dict):
            return False
        return True

    @staticmethod
    def encode(message: Dict[str, Any]) -> bytes:
        """Convert a message dictionary to UTF-8 JSON bytes plus newline."""
        if not Protocol.validate_message(message):
            raise ValueError(f"Invalid protocol message: {message!r}")
        json_text = json.dumps(message, ensure_ascii=False, separators=(",", ":"))
        return json_text.encode("utf-8") + Protocol.MESSAGE_DELIMITER

    @staticmethod
    def decode(raw_message: bytes | str) -> Dict[str, Any]:
        """Convert one JSON line to a message dictionary."""
        if isinstance(raw_message, bytes):
            raw_message = raw_message.decode("utf-8")
        raw_message = raw_message.strip()
        if not raw_message:
            raise ValueError("Cannot decode empty message")

        message = json.loads(raw_message)
        if not Protocol.validate_message(message):
            raise ValueError(f"Invalid protocol message: {message!r}")
        return message

    @staticmethod
    def create_error(message: str) -> Dict[str, Any]:
        """Create a standard server error response message."""
        return Protocol.create_message(MessageType.ERROR, {"message": str(message)})
