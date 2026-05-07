"""
Stacking Rule for +2 and +4

Rules:
- After +2, next player may stack +2 or +4.
- After +4, next player may stack only +4.
- Penalties accumulate.
- First player who cannot or chooses not to stack draws full penalty and loses turn.
"""

from game.card import CardType


class StackingRule:
    @staticmethod
    def get_penalty_value(card):
        if card.card_type == CardType.DRAW_TWO:
            return 2
        if card.card_type == CardType.WILD_DRAW_FOUR:
            return 4
        return 0

    @staticmethod
    def is_penalty_card(card):
        return card.card_type in (CardType.DRAW_TWO, CardType.WILD_DRAW_FOUR)

    @staticmethod
    def can_stack(card, last_penalty_value):
        if not StackingRule.is_penalty_card(card):
            return False
        # After +4 only +4 can stack; after +2 both +2 and +4 can stack.
        return StackingRule.get_penalty_value(card) >= last_penalty_value

    @staticmethod
    def add_penalty(current_penalty, card):
        return current_penalty + StackingRule.get_penalty_value(card)

    @staticmethod
    def resolve_penalty(player, deck, pending_penalty):
        drawn = deck.draw_many(pending_penalty)
        player.add_cards(drawn)
        return {"drawn": [repr(c) for c in drawn], "count": pending_penalty}

    @staticmethod
    def reset_penalty_state():
        return {"pending_penalty": 0, "last_penalty_value": 0}
