"""
Sync Manager

TODO:
Broadcast game state and room state to all clients.
"""


class SyncManager:
    def __init__(self, server=None):
        # TODO: Store server/socket reference if needed
        pass

    def send_to_player(self, player_connection, message):
        # TODO: Send one message to one player
        pass

    def broadcast_to_room(self, room, message):
        # TODO: Send message to every player in room
        pass

    def broadcast_player_list(self, room):
        # TODO: Build player list data
        # TODO: Broadcast player list to room
        pass

    def broadcast_game_state(self, room):
        # TODO: For each player, build state using to_dict_for_player(player_id)
        # TODO: Send private state to each player
        pass

    def broadcast_invalid_action(self, player_connection, reason):
        # TODO: Send invalid action message to one player
        pass

    def broadcast_game_started(self, room):
        # TODO: Notify all players that game started
        # TODO: Broadcast initial game state
        pass

    def broadcast_game_ended(self, room, winner_id):
        # TODO: Notify all players that game ended
        pass

    def broadcast_reaction_started(self, room, event_data):
        # TODO: Notify all players that Rule 8 reaction event started
        pass

    def broadcast_reaction_result(self, room, result_data):
        # TODO: Notify all players about Rule 8 result
        pass