class Player:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def add_cards(self, cards):
        self.hand.extend(cards)

    def remove_card(self, card_index):
        if card_index < 0 or card_index >= len(self.hand):
            raise IndexError(f"Card index {card_index} out of range.")
        return self.hand.pop(card_index)

    def card_count(self):
        return len(self.hand)

    def has_no_cards(self):
        return len(self.hand) == 0

    def to_public_dict(self):
        return {
            "player_id": self.player_id,
            "name": self.name,
            "card_count": self.card_count(),
        }

    def to_private_dict(self):
        return {
            "player_id": self.player_id,
            "name": self.name,
            "hand": [c.to_dict() for c in self.hand],
        }
