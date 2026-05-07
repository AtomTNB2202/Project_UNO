import random

from game.card import Card, Color, CardType


class Deck:
    def __init__(self):
        self.draw_pile = []
        self.discard_pile = []

    def build_standard_deck(self):
        self.draw_pile = []
        colors = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]
        for color in colors:
            self.draw_pile.append(Card(color, CardType.NUMBER, 0))
            for value in range(1, 10):
                self.draw_pile.append(Card(color, CardType.NUMBER, value))
                self.draw_pile.append(Card(color, CardType.NUMBER, value))
            for _ in range(2):
                self.draw_pile.append(Card(color, CardType.SKIP))
                self.draw_pile.append(Card(color, CardType.REVERSE))
                self.draw_pile.append(Card(color, CardType.DRAW_TWO))
        for _ in range(4):
            self.draw_pile.append(Card(Color.WILD, CardType.WILD))
            self.draw_pile.append(Card(Color.WILD, CardType.WILD_DRAW_FOUR))

    def shuffle(self):
        random.shuffle(self.draw_pile)

    def draw_one(self):
        if not self.draw_pile:
            self.rebuild_draw_pile()
        if not self.draw_pile:
            return None
        return self.draw_pile.pop()

    def draw_many(self, amount):
        return [c for c in (self.draw_one() for _ in range(amount)) if c is not None]

    def put_to_discard(self, card):
        self.discard_pile.append(card)

    def top_discard(self):
        return self.discard_pile[-1] if self.discard_pile else None

    def rebuild_draw_pile(self):
        if len(self.discard_pile) <= 1:
            return
        top = self.discard_pile.pop()
        self.draw_pile = self.discard_pile
        self.discard_pile = [top]
        random.shuffle(self.draw_pile)
