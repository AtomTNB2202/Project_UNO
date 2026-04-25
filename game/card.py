from enum import Enum


class Color(str, Enum):
    # TODO: define card colors
    pass


class CardType(str, Enum):
    # TODO: define card types
    pass


class Card:
    def __init__(self, color, card_type, value=None):
        # TODO: store color
        # TODO: store card type
        # TODO: store value for number cards
        pass

    def is_number_card(self):
        # TODO: return True if this is a number card
        pass

    def is_action_card(self):
        # TODO: return True if this is an action/special card
        pass

    def is_wild_card(self):
        # TODO: return True if this is Wild or Wild Draw Four
        pass

    def penalty_value(self):
        # TODO: return 2 for Draw Two, 4 for Wild Draw Four, otherwise 0
        pass

    def __repr__(self): # type: ignore
        # TODO: return readable card name
        pass