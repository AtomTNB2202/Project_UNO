"""
Stacking Rule for +2 and +4

Rules:
- After +2, next player may stack +2 or +4.
- After +4, next player may stack only +4.
- Penalties accumulate.
- First player who cannot or chooses not to stack draws full penalty and loses turn.
"""


class StackingRule:
    @staticmethod
    def get_penalty_value(card):
        # TODO: Return 2 if card is Draw Two
        # TODO: Return 4 if card is Wild Draw Four
        # TODO: Return 0 otherwise
        pass

    @staticmethod
    def is_penalty_card(card):
        # TODO: Return True if card is +2 or +4
        pass

    @staticmethod
    def can_stack(card, last_penalty_value):
        # TODO: Check card is penalty card
        # TODO: Check card penalty value >= last_penalty_value
        pass

    @staticmethod
    def add_penalty(current_penalty, card):
        # TODO: Add card penalty value to current pending penalty
        # TODO: Return new pending penalty
        pass

    @staticmethod
    def resolve_penalty(player, deck, pending_penalty):
        # TODO: Draw pending_penalty cards from deck
        # TODO: Add drawn cards to player hand
        # TODO: Return result dictionary
        pass

    @staticmethod
    def reset_penalty_state():
        # TODO: Return default penalty state
        # Example:
        # {
        #   "pending_penalty": 0,
        #   "last_penalty_value": 0
        # }
        pass