"""
Game Screen

TODO:
Main gameplay screen.
"""


class GameScreen:
    def __init__(self, client):
        # TODO: store client/network object
        # TODO: initialize HandView
        # TODO: initialize OpponentPanel
        # TODO: initialize StatusPanel
        # TODO: initialize PopupSelectColor
        # TODO: initialize PopupSelectTarget
        # TODO: initialize ReactionButton
        # TODO: store latest game state
        pass

    def set_game_state(self, game_state):
        # TODO: update latest game state
        # TODO: update hand view
        # TODO: update opponent panel
        # TODO: update status panel
        pass

    def render(self, surface):
        # TODO: draw game background
        # TODO: render status panel
        # TODO: render opponent panel
        # TODO: render hand view
        # TODO: render active popups
        # TODO: render reaction button if active
        pass

    def handle_event(self, event):
        # TODO: handle card selection
        # TODO: handle draw button
        # TODO: handle play button
        # TODO: handle color popup
        # TODO: handle target popup
        # TODO: handle reaction button
        pass

    def request_play_card(self, card_index):
        # TODO: determine whether selected card needs extra input
        # TODO: if Wild, open color popup
        # TODO: if card 0, open direction selection
        # TODO: if card 7, open target popup
        # TODO: otherwise send play_card request to client
        pass

    def request_draw_card(self):
        # TODO: call client.draw_card()
        pass

    def handle_reaction_started(self, event_data):
        # TODO: show reaction button
        pass

    def handle_reaction_result(self, result_data):
        # TODO: hide reaction button
        # TODO: show reaction result if needed
        pass