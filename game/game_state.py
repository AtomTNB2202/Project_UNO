from game.custom_rules.rule_zero import RuleZero
from game.custom_rules.rule_seven import RuleSeven
from game.custom_rules.rule_eight import RuleEight
from game.custom_rules.stacking_rule import StackingRule

class GameState:
    def __init__(self):
        # TODO: initialize players
        # TODO: initialize deck
        # TODO: initialize turn manager
        # TODO: initialize game status
        # TODO: initialize current color
        # TODO: initialize pending penalty
        # TODO: initialize winner
        pass

    def add_player(self, player_id, name):
        # TODO: add player before game starts
        # TODO: validate max 4 players
        pass

    def remove_player(self, player_id):
        # TODO: remove player before game starts
        pass

    def can_start(self):
        # TODO: return True if player count is between 2 and 4
        pass

    def start_game(self):
        # TODO: validate player count
        # TODO: build deck
        # TODO: shuffle deck
        # TODO: deal initial cards
        # TODO: create first discard card
        # TODO: set current color
        # TODO: mark game as started
        pass

    def get_current_player(self):
        # TODO: return current player object
        pass

    def find_player_index(self, player_id):
        # TODO: find player index by player_id
        pass

    def play_card(
        self,
        player_id,
        card_index,
        chosen_color=None,
        zero_direction=None,
        seven_target_id=None,
    ):
        # TODO: validate game has started
        # TODO: validate correct player's turn
        # TODO: validate card index
        # TODO: validate legal card
        # TODO: validate no-win-with-action-card rule
        # TODO: remove card from player hand
        # TODO: put card to discard pile
        # TODO: update current color
        # TODO: apply card effect
        # TODO: check winner
        # TODO: return result dictionary
        pass

    def draw_card(self, player_id):
        # TODO: validate game has started
        # TODO: validate correct player's turn
        # TODO: if pending penalty exists, draw full penalty
        # TODO: otherwise draw one card
        # TODO: update turn if needed
        # TODO: return result dictionary
        pass

    def apply_card_effect(
        self,
        card,
        player_id,
        chosen_color=None,
        zero_direction=None,
        seven_target_id=None,
    ):
        # TODO: handle Skip
        # TODO: handle Reverse
        # TODO: handle Draw Two
        # TODO: handle Wild
        # TODO: handle Wild Draw Four
        # TODO: handle Rule of 0
        # TODO: handle Rule of 7
        # TODO: handle Rule of 8
        # TODO: update turn
        pass

    def apply_rule_zero(self, direction):
        # TODO: validate direction
        # TODO: pass all hands clockwise or counter-clockwise
        pass

    def apply_rule_seven(self, player_id, target_player_id):
        # TODO: validate target player
        # TODO: swap hands between player and target
        pass

    def start_reaction_event(self, player_id):
        # TODO: start Rule of 8 reaction event
        # TODO: store reaction state
        # TODO: networking layer will broadcast this event
        pass

    def submit_reaction(self, player_id):
        # TODO: record reaction response
        # TODO: reject duplicate response
        pass

    def finish_reaction_event(self):
        # TODO: decide latest responder
        # TODO: apply draw 2 penalty
        # TODO: clear reaction state
        pass

    def to_dict_for_player(self, viewer_id):
        # TODO: return game state for one specific player
        # TODO: viewer sees own hand
        # TODO: viewer sees only card count of opponents
        pass