"""
Rule of 8

When a player plays an 8 card:
- A reaction event starts.
- All players must click a reaction button.
- The latest responder receives draw 2 penalty.
- Players who do not respond before timeout are also penalized.
"""

import time


class RuleEight:
    def __init__(self):
        self.active = False
        self.start_time = None
        self.response_window = 3
        self.responses = {}      # player_id -> timestamp
        self.player_ids = []

    def start_event(self, players, response_window=3):
        self.active = True
        self.start_time = time.time()
        self.response_window = response_window
        self.player_ids = [p.player_id for p in players]
        self.responses = {}
        return {
            "event": "reaction_start",
            "response_window": response_window,
            "players": self.player_ids,
        }

    def submit_response(self, player_id):
        if not self.active:
            return {"success": False, "reason": "No active reaction event."}
        if player_id not in self.player_ids:
            return {"success": False, "reason": "Player is not part of this event."}
        if player_id in self.responses:
            return {"success": False, "reason": "Already responded."}
        if self.is_timeout():
            return {"success": False, "reason": "Response window has expired."}
        self.responses[player_id] = time.time()
        return {"success": True, "player_id": player_id}

    def all_responded(self):
        return self.active and len(self.responses) == len(self.player_ids)

    def is_timeout(self):
        if self.start_time is None:
            return False
        return time.time() - self.start_time >= self.response_window

    def get_missing_players(self):
        return [pid for pid in self.player_ids if pid not in self.responses]

    def remove_player(self, player_id):
        if player_id in self.player_ids:
            self.player_ids.remove(player_id)
        self.responses.pop(player_id, None)

    def get_latest_responders(self):
        missing = self.get_missing_players()
        if missing:
            # All players who didn't respond in time are penalized.
            return missing
        # Everyone responded — penalize the one who responded last.
        latest = max(self.responses, key=lambda pid: self.responses[pid])
        return [latest]

    def finish_event(self, players, deck):
        if not self.active:
            return {"success": False, "reason": "No active reaction event."}
        penalized_ids = self.get_latest_responders()
        penalized_players = [p for p in players if p.player_id in penalized_ids]
        for player in penalized_players:
            drawn = deck.draw_many(2)
            player.add_cards(drawn)
        self.reset()
        return {
            "penalized": penalized_ids,
            "draw_count": 2,
        }

    def reset(self):
        self.active = False
        self.start_time = None
        self.responses = {}
        self.player_ids = []
