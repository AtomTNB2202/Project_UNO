from game.card import CardType
from game.custom_rules.stacking_rule import StackingRule


class RuleEngine:
    @staticmethod
    def is_legal_card(
        selected_card,
        top_card,
        current_color,
        pending_penalty=0,
        last_penalty_value=0,
    ):
        # When a penalty is pending, only stacking cards are legal.
        if pending_penalty > 0:
            return RuleEngine.can_stack_penalty(selected_card, last_penalty_value)

        # Wild cards are always legal (when no pending penalty).
        if selected_card.is_wild_card():
            return True

        # Match by current color.
        if selected_card.color == current_color:
            return True

        # Match number cards by value.
        if selected_card.is_number_card() and top_card.is_number_card():
            return selected_card.value == top_card.value

        # Match action cards by type (Skip on Skip, Reverse on Reverse, etc.).
        if selected_card.is_action_card() and top_card.is_action_card():
            return selected_card.card_type == top_card.card_type

        return False

    @staticmethod
    def can_stack_penalty(selected_card, last_penalty_value):
        return StackingRule.can_stack(selected_card, last_penalty_value)

    @staticmethod
    def is_forbidden_final_card(card):
        # A player cannot win by playing any action or wild card.
        return card.card_type in (
            CardType.SKIP,
            CardType.REVERSE,
            CardType.DRAW_TWO,
            CardType.WILD,
            CardType.WILD_DRAW_FOUR,
        )

    @staticmethod
    def can_play_as_final_card(card):
        return not RuleEngine.is_forbidden_final_card(card)
