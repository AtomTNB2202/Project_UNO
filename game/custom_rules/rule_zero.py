"""
Rule of 0

When a player plays a 0 card:
- The player chooses a direction.
- All players pass their entire hand in that direction.
"""

VALID_DIRECTIONS = ("CLOCKWISE", "COUNTER_CLOCKWISE")


class RuleZero:
    @staticmethod
    def validate_direction(direction):
        if direction not in VALID_DIRECTIONS:
            raise ValueError(f"Invalid direction '{direction}'. Must be one of {VALID_DIRECTIONS}.")

    @staticmethod
    def apply(players, direction):
        RuleZero.validate_direction(direction)
        n = len(players)
        # Snapshot all hands before any swapping.
        old_hands = [list(p.hand) for p in players]

        if direction == "CLOCKWISE":
            # Each player receives the hand of the previous player (index i-1).
            for i, player in enumerate(players):
                player.hand = old_hands[(i - 1) % n]
        else:
            # Each player receives the hand of the next player (index i+1).
            for i, player in enumerate(players):
                player.hand = old_hands[(i + 1) % n]

        return {
            "direction": direction,
            "players": [p.to_public_dict() for p in players],
        }
