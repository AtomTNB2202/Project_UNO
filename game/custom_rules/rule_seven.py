"""
Rule of 7

When a player plays a 7 card:
- The player chooses one target player.
- The two players swap their entire hands.
"""


class RuleSeven:
    @staticmethod
    def validate_target(players, player_id, target_player_id):
        # TODO: Check target_player_id is not None
        # TODO: Check player_id exists
        # TODO: Check target_player_id exists
        # TODO: Check player_id != target_player_id
        pass

    @staticmethod
    def find_player(players, player_id):
        # TODO: Find and return player by player_id
        pass

    @staticmethod
    def apply(players, player_id, target_player_id):
        # TODO: Validate target
        # TODO: Find current player
        # TODO: Find target player
        # TODO: Swap their hands
        # TODO: Return result dictionary
        pass