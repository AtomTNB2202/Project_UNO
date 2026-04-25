"""
Rule of 8

When a player plays an 8 card:
- A reaction event starts.
- All players must click a reaction button.
- The latest responder receives draw 2 penalty.
- Players who do not respond before timeout are also penalized.
"""


class RuleEight:
    def __init__(self):
        # TODO: Store whether reaction event is active
        # TODO: Store event start time
        # TODO: Store response window duration
        # TODO: Store responses from players
        # TODO: Store player IDs participating in this event
        pass

    def start_event(self, players, response_window=3):
        # TODO: Mark reaction event as active
        # TODO: Store current time as event start time
        # TODO: Store response window
        # TODO: Store all player IDs
        # TODO: Clear previous responses
        # TODO: Return event data for broadcasting
        pass

    def submit_response(self, player_id):
        # TODO: Check event is active
        # TODO: Check player_id is part of current event
        # TODO: Reject duplicate response
        # TODO: Reject response after timeout if needed
        # TODO: Store response timestamp
        # TODO: Return response result
        pass

    def is_timeout(self):
        # TODO: Check whether response window has expired
        pass

    def get_missing_players(self):
        # TODO: Return players who did not respond
        pass

    def get_latest_responders(self):
        # TODO: If some players did not respond, return all missing players
        # TODO: Otherwise, return the player with latest timestamp
        pass

    def finish_event(self, players):
        # TODO: Check event is active
        # TODO: Find penalized players
        # TODO: Make penalized players draw 2 cards
        # TODO: Clear reaction event state
        # TODO: Return result dictionary
        pass

    def reset(self):
        # TODO: Clear all reaction event state
        pass