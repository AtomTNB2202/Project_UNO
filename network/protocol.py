"""
Network Protocol

TODO:
Define message types and message format between client and server.
"""


class MessageType:
    # TODO: Room events
    CREATE_ROOM = None
    JOIN_ROOM = None
    LEAVE_ROOM = None
    START_GAME = None

    # TODO: Gameplay events
    PLAY_CARD = None
    DRAW_CARD = None
    CHOOSE_COLOR = None
    CHOOSE_ZERO_DIRECTION = None
    CHOOSE_SEVEN_TARGET = None
    SUBMIT_REACTION = None

    # TODO: Server response events
    ROOM_CREATED = None
    ROOM_JOINED = None
    PLAYER_LIST_UPDATED = None
    GAME_STARTED = None
    STATE_UPDATED = None
    INVALID_ACTION = None
    REACTION_STARTED = None
    REACTION_RESULT = None
    GAME_ENDED = None
    ERROR = None


class Protocol:
    @staticmethod
    def create_message(message_type, data=None):
        # TODO: Return standard message dictionary
        pass

    @staticmethod
    def validate_message(message):
        # TODO: Check message is dictionary
        # TODO: Check message has type
        # TODO: Check message has data
        pass

    @staticmethod
    def encode(message):
        # TODO: Convert message dictionary to JSON string / bytes
        pass

    @staticmethod
    def decode(raw_message):
        # TODO: Convert JSON string / bytes to message dictionary
        pass

    @staticmethod
    def create_error(message):
        # TODO: Create error response message
        pass