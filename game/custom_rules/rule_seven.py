"""
Rule of 7

When a player plays a 7 card:
- The player chooses one target player.
- The two players swap their entire hands.
"""


class RuleSeven:
    @staticmethod
    def validate_target(players, player_id, target_player_id):
        if target_player_id is None:
            raise ValueError("A target player must be specified.")
        player_ids = {p.player_id for p in players}
        if player_id not in player_ids:
            raise ValueError(f"Player '{player_id}' not found.")
        if target_player_id not in player_ids:
            raise ValueError(f"Target player '{target_player_id}' not found.")
        if player_id == target_player_id:
            raise ValueError("Cannot swap hands with yourself.")

    @staticmethod
    def find_player(players, player_id):
        for p in players:
            if p.player_id == player_id:
                return p
        return None

    @staticmethod
    def apply(players, player_id, target_player_id):
        RuleSeven.validate_target(players, player_id, target_player_id)
        player = RuleSeven.find_player(players, player_id)
        target = RuleSeven.find_player(players, target_player_id)
        player.hand, target.hand = target.hand, player.hand
        return {
            "player_id": player_id,
            "target_player_id": target_player_id,
        }
