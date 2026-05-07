class TurnManager:
    def __init__(self):
        self._current_index = 0
        self._direction = 1  # 1 = clockwise, -1 = counter-clockwise

    def current_player_index(self):
        return self._current_index

    def next_turn(self, player_count):
        self._current_index = (self._current_index + self._direction) % player_count

    def skip_next(self, player_count):
        self._current_index = (self._current_index + self._direction * 2) % player_count

    def reverse_direction(self, player_count):
        self._direction *= -1

    def get_direction_text(self):
        return "CLOCKWISE" if self._direction == 1 else "COUNTER_CLOCKWISE"
