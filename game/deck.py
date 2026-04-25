class Deck:
    def __init__(self):
        # TODO: initialize draw pile
        # TODO: initialize discard pile
        pass

    def build_standard_deck(self):
        # TODO: create UNO deck
        # TODO: add number cards
        # TODO: add Skip cards
        # TODO: add Reverse cards
        # TODO: add Draw Two cards
        # TODO: add Wild cards
        # TODO: add Wild Draw Four cards
        pass

    def shuffle(self):
        # TODO: shuffle draw pile
        pass

    def draw_one(self):
        # TODO: draw one card from draw pile
        # TODO: rebuild draw pile if empty
        pass

    def draw_many(self, amount):
        # TODO: draw multiple cards
        pass

    def put_to_discard(self, card):
        # TODO: put card on discard pile
        pass

    def top_discard(self):
        # TODO: return top card of discard pile
        pass

    def rebuild_draw_pile(self):
        # TODO: rebuild draw pile from discard pile
        # TODO: keep top discard card
        # TODO: shuffle rebuilt draw pile
        pass