from enum import Enum


class Color(str, Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    WILD = "WILD"


class CardType(str, Enum):
    NUMBER = "NUMBER"
    SKIP = "SKIP"
    REVERSE = "REVERSE"
    DRAW_TWO = "DRAW_TWO"
    WILD = "WILD"
    WILD_DRAW_FOUR = "WILD_DRAW_FOUR"


class Card:
    def __init__(self, color, card_type, value=None):
        self.color = color
        self.card_type = card_type
        self.value = value

    def is_number_card(self):
        return self.card_type == CardType.NUMBER

    def is_action_card(self):
        return self.card_type in (CardType.SKIP, CardType.REVERSE, CardType.DRAW_TWO)

    def is_wild_card(self):
        return self.card_type in (CardType.WILD, CardType.WILD_DRAW_FOUR)

    def penalty_value(self):
        if self.card_type == CardType.DRAW_TWO:
            return 2
        if self.card_type == CardType.WILD_DRAW_FOUR:
            return 4
        return 0

    def to_dict(self):
        return {
            "color": self.color.value,
            "type": self.card_type.value,
            "value": self.value,
        }

    def __repr__(self):
        if self.is_wild_card():
            return self.card_type.value
        if self.is_number_card():
            return f"{self.color.value} {self.value}"
        return f"{self.color.value} {self.card_type.value}"
