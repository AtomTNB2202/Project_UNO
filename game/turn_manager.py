class TurnManager:
    def __init__(self):
        self._current_index = 0
        self._direction = 1  # 1 = clockwise, -1 = counter-clockwise

    def current_player_index(self):
        return self._current_index

    def next_turn(self, player_count):
        self._current_index = (self._current_index + self._direction) % player_count

    def skip_next(self, player_count):
        # Advance by 2 steps, effectively skipping the immediate next player.
        # In a 2-player game this wraps back to the current player (acts as skip = play again).
        self._current_index = (self._current_index + 2 * self._direction) % player_count

    def reverse_direction(self, player_count):
        self._direction *= -1
        # 2-player special case: Reverse acts like Skip (same player goes again).
        # apply_card_effect handles this by NOT calling next_turn when n == 2,
        # so the index naturally stays on the current player — no advance needed here.

    def get_direction_text(self):
        return "CLOCKWISE" if self._direction == 1 else "COUNTER_CLOCKWISE"
