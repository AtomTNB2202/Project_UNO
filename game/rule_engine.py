class RuleEngine:
    @staticmethod
    def is_legal_card(
        selected_card,
        top_card,
        current_color,
        pending_penalty=0,
        last_penalty_value=0,
    ):
        # TODO: if pending penalty exists, validate stacking rule
        # TODO: allow same color
        # TODO: allow same number
        # TODO: allow same action type
        # TODO: allow Wild / Wild Draw Four
        # TODO: return True or False
        pass

    @staticmethod
    def can_stack_penalty(selected_card, last_penalty_value):
        # TODO: after +2, allow +2 or +4
        # TODO: after +4, allow only +4
        pass

    @staticmethod
    def is_forbidden_final_card(card):
        # TODO: check if card cannot be used as final winning card
        pass

    @staticmethod
    def can_play_as_final_card(card):
        # TODO: return True if card is allowed as final card
        pass