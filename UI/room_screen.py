"""
Room Screen

TODO:
Screen for creating or joining a room.
"""


class RoomScreen:
    def __init__(self, client):
        # TODO: store client
        # TODO: store player name input
        # TODO: store room code input
        # TODO: store mode: create or join
        pass

    def set_mode(self, mode):
        # TODO: set CREATE or JOIN mode
        pass

    def render(self, surface):
        # TODO: draw form background
        # TODO: draw player name input
        # TODO: draw room code input if joining
        # TODO: draw confirm button
        # TODO: draw back button
        pass

    def handle_event(self, event):
        # TODO: handle text input
        # TODO: handle create room confirm
        # TODO: handle join room confirm
        # TODO: handle back button
        pass

    def submit(self):
        # TODO: if mode is CREATE, call client.create_room(...)
        # TODO: if mode is JOIN, call client.join_room(...)
        pass