from game.card import CardType


class RuleEngine:
    @staticmethod
    def is_legal_card(
        selected_card,
        top_card,
        current_color,
        pending_penalty=0,
        last_penalty_value=0,
    ):
        if pending_penalty > 0:
            return RuleEngine.can_stack_penalty(selected_card, last_penalty_value)
        if selected_card.is_wild_card():
            return True
        if selected_card.color == current_color:
            return True
        if selected_card.card_type == top_card.card_type:
            if selected_card.is_number_card():
                return selected_card.value == top_card.value
            return True
        return False

    @staticmethod
    def can_stack_penalty(selected_card, last_penalty_value):
        if selected_card.card_type == CardType.WILD_DRAW_FOUR:
            return True
        if selected_card.card_type == CardType.DRAW_TWO:
            # +2 can only stack on top of +2, not +4
            return last_penalty_value <= 2
        return False

    @staticmethod
    def is_forbidden_final_card(card):
        return card.card_type in (
            CardType.WILD,
            CardType.WILD_DRAW_FOUR,
            CardType.DRAW_TWO,
            CardType.SKIP,
            CardType.REVERSE,
        )

    @staticmethod
    def can_play_as_final_card(card):
        return not RuleEngine.is_forbidden_final_card(card)
