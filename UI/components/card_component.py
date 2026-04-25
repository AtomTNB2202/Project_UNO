"""
Card Component

TODO:
Display one UNO card.
"""


class CardComponent:
    def __init__(self, card, position=None, size=None):
        # TODO: store card data
        # TODO: store card position
        # TODO: store card size
        # TODO: store whether card is selected/clickable
        pass

    def render(self, surface):
        # TODO: draw card rectangle
        # TODO: draw card color
        # TODO: draw card value/type text
        pass

    def handle_event(self, event):
        # TODO: detect mouse click on this card
        # TODO: return selected card index or card object if clicked
        pass

    def set_selected(self, selected):
        # TODO: update selected state
        pass

    def set_clickable(self, clickable):
        # TODO: update clickable state
        pass