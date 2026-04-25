"""
Lobby Screen

TODO:
Display players waiting in room before game starts.
"""


class LobbyScreen:
    def __init__(self, client):
        # TODO: store client
        # TODO: store room code
        # TODO: store player list
        # TODO: store whether current player is host
        pass

    def set_room_data(self, room_code, players, is_host=False):
        # TODO: update room code
        # TODO: update player list
        # TODO: update host status
        pass

    def render(self, surface):
        # TODO: draw lobby background
        # TODO: draw room code
        # TODO: draw player list
        # TODO: draw Start Game button if host
        # TODO: draw Leave Room button
        pass

    def handle_event(self, event):
        # TODO: handle Start Game button
        # TODO: handle Leave Room button
        pass