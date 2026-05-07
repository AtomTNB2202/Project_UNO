from game.card import CardType
from game.deck import Deck
from game.player import Player
from game.turn_manager import TurnManager
from game.rule_engine import RuleEngine
from game.custom_rules.rule_zero import RuleZero
from game.custom_rules.rule_seven import RuleSeven
from game.custom_rules.rule_eight import RuleEight
from game.custom_rules.stacking_rule import StackingRule

try:
    from config import MIN_PLAYERS, MAX_PLAYERS, INITIAL_HAND_SIZE
except ImportError:
    MIN_PLAYERS, MAX_PLAYERS, INITIAL_HAND_SIZE = 2, 4, 7


class GameState:
    def __init__(self, players=None):
        self.players = []
        self.deck = Deck()
        self.turn_manager = TurnManager()
        self.started = False
        self.current_color = None
        self.pending_penalty = 0
        self.last_penalty_value = 0
        self.winner = None      # dict {"player_id": ..., "name": ...}
        self.winner_id = None   # str — used by server._extract_winner_id
        self._rule_eight = RuleEight()

        if players:
            # Server passes player_ids (list of strings) first; raise TypeError
            # so it falls through to the player-dict form with correct names.
            if all(isinstance(p, str) for p in players):
                raise TypeError("Expected player dicts with 'id' and 'name' keys")
            for p in players:
                if isinstance(p, dict):
                    pid = p.get("id") or p.get("player_id", "")
                    name = p.get("name", "Player")
                    if pid:
                        self.add_player(pid, name)

    # ------------------------------------------------------------------
    # Room setup
    # ------------------------------------------------------------------

    def add_player(self, player_id, name):
        if self.started:
            raise ValueError("Cannot add player after game has started.")
        if len(self.players) >= MAX_PLAYERS:
            raise ValueError(f"Room is full (max {MAX_PLAYERS} players).")
        self.players.append(Player(player_id, name))

    def remove_player(self, player_id):
        self.players = [p for p in self.players if p.player_id != player_id]

    def can_start(self):
        return MIN_PLAYERS <= len(self.players) <= MAX_PLAYERS

    # ------------------------------------------------------------------
    # Game start
    # ------------------------------------------------------------------

    def start_game(self):
        if not self.can_start():
            raise ValueError(
                f"Need between {MIN_PLAYERS} and {MAX_PLAYERS} players to start."
            )
        self.deck.build_standard_deck()
        self.deck.shuffle()
        for player in self.players:
            player.add_cards(self.deck.draw_many(INITIAL_HAND_SIZE))

        # First discard card must be a plain number card
        first_card = self.deck.draw_one()
        while first_card and (first_card.is_wild_card() or first_card.is_action_card()):
            self.deck.put_to_discard(first_card)
            first_card = self.deck.draw_one()
        self.deck.put_to_discard(first_card)
        self.current_color = first_card.color.value
        self.started = True

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def get_current_player(self):
        return self.players[self.turn_manager.current_player_index()]

    def find_player_index(self, player_id):
        for i, p in enumerate(self.players):
            if p.player_id == player_id:
                return i
        return -1

    def _find_player(self, player_id):
        for p in self.players:
            if p.player_id == player_id:
                return p
        return None

    # ------------------------------------------------------------------
    # Core actions
    # ------------------------------------------------------------------

    def play_card(
        self,
        player_id,
        card_index,
        chosen_color=None,
        zero_direction=None,
        seven_target_id=None,
    ):
        if not self.started:
            raise ValueError("Game has not started.")
        current = self.get_current_player()
        if current.player_id != player_id:
            raise ValueError("Not your turn.")
        if card_index < 0 or card_index >= current.card_count():
            raise ValueError("Invalid card index.")

        card = current.hand[card_index]
        top = self.deck.top_discard()

        if not RuleEngine.is_legal_card(
            card, top, self.current_color,
            self.pending_penalty, self.last_penalty_value,
        ):
            raise ValueError("That card cannot be played.")

        if current.card_count() == 1 and not RuleEngine.can_play_as_final_card(card):
            raise ValueError("Cannot win with an action or wild card.")

        played_card = current.remove_card(card_index)
        self.deck.put_to_discard(played_card)

        # Update active color
        if played_card.is_wild_card():
            self.current_color = chosen_color or "RED"
        else:
            self.current_color = played_card.color.value

        effect = self.apply_card_effect(
            played_card, player_id, chosen_color, zero_direction, seven_target_id
        )

        if current.has_no_cards():
            self.winner = {"player_id": player_id, "name": current.name}
            self.winner_id = player_id

        return {
            "played_card": played_card.to_dict(),
            "effect": effect,
            "winner": self.winner,
            "winner_id": self.winner_id,
        }

    def draw_card(self, player_id):
        if not self.started:
            raise ValueError("Game has not started.")
        current = self.get_current_player()
        if current.player_id != player_id:
            raise ValueError("Not your turn.")

        n = len(self.players)
        if self.pending_penalty > 0:
            drawn = self.deck.draw_many(self.pending_penalty)
            current.add_cards(drawn)
            reset = StackingRule.reset_penalty_state()
            self.pending_penalty = reset["pending_penalty"]
            self.last_penalty_value = reset["last_penalty_value"]
            self.turn_manager.next_turn(n)
            return {
                "drawn": [c.to_dict() for c in drawn],
                "count": len(drawn),
                "penalty": True,
            }

        card = self.deck.draw_one()
        if card:
            current.add_card(card)
        self.turn_manager.next_turn(n)
        return {
            "drawn": [card.to_dict()] if card else [],
            "count": 1 if card else 0,
            "penalty": False,
        }

    # ------------------------------------------------------------------
    # Card effects
    # ------------------------------------------------------------------

    def apply_card_effect(
        self,
        card,
        player_id,
        chosen_color=None,
        zero_direction=None,
        seven_target_id=None,
    ):
        n = len(self.players)

        if card.card_type == CardType.SKIP:
            self.turn_manager.skip_next(n)
            return {"effect": "SKIP"}

        if card.card_type == CardType.REVERSE:
            self.turn_manager.reverse_direction(n)
            if n == 2:
                # Reverse acts like skip in 2-player: current player goes again
                pass
            else:
                self.turn_manager.next_turn(n)
            return {"effect": "REVERSE", "direction": self.turn_manager.get_direction_text()}

        if card.card_type == CardType.DRAW_TWO:
            if self.pending_penalty == 0:
                self.last_penalty_value = 2
            self.pending_penalty = StackingRule.add_penalty(self.pending_penalty, card)
            self.turn_manager.next_turn(n)
            return {"effect": "DRAW_TWO", "pending_penalty": self.pending_penalty}

        if card.card_type == CardType.WILD:
            self.turn_manager.next_turn(n)
            return {"effect": "WILD", "color": chosen_color}

        if card.card_type == CardType.WILD_DRAW_FOUR:
            if self.pending_penalty == 0:
                self.last_penalty_value = 4
            self.pending_penalty = StackingRule.add_penalty(self.pending_penalty, card)
            self.turn_manager.next_turn(n)
            return {
                "effect": "WILD_DRAW_FOUR",
                "pending_penalty": self.pending_penalty,
                "color": chosen_color,
            }

        if card.card_type == CardType.NUMBER:
            if card.value == 0:
                direction = zero_direction
                # Quick-and-dirty: UI sends chosen_color as proxy (RED=CW, else=CCW)
                if direction is None and chosen_color:
                    direction = "CLOCKWISE" if chosen_color == "RED" else "COUNTER_CLOCKWISE"
                if direction:
                    result = self.apply_rule_zero(direction)
                    self.turn_manager.next_turn(n)
                    return {"effect": "RULE_ZERO", **result}

            elif card.value == 7:
                if seven_target_id:
                    result = self.apply_rule_seven(player_id, seven_target_id)
                    self.turn_manager.next_turn(n)
                    return {"effect": "RULE_SEVEN", **result}

            elif card.value == 8:
                event_result = self.start_reaction_event(player_id)
                self.turn_manager.next_turn(n)
                return {"effect": "RULE_EIGHT", "reaction_started": event_result}

            self.turn_manager.next_turn(n)
            return {"effect": "NUMBER"}

        self.turn_manager.next_turn(n)
        return {"effect": "NONE"}

    # ------------------------------------------------------------------
    # Custom rule helpers
    # ------------------------------------------------------------------

    def apply_rule_zero(self, direction):
        RuleZero.validate_direction(direction)
        return RuleZero.apply(self.players, direction)

    def apply_rule_seven(self, player_id, target_player_id):
        return RuleSeven.apply(self.players, player_id, target_player_id)

    def start_reaction_event(self, player_id):
        return self._rule_eight.start_event(self.players)

    def submit_reaction(self, player_id):
        result = self._rule_eight.submit_response(player_id)
        if self._rule_eight.is_timeout():
            reaction_result = self.finish_reaction_event()
            return {"submit": result, "reaction_result": reaction_result}
        return {"submit": result}

    def finish_reaction_event(self):
        return self._rule_eight.finish_event(self.players, self.deck)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict_for_player(self, viewer_id):
        top_card = self.deck.top_discard()
        current = self.get_current_player() if self.started else None
        return {
            "players": [
                p.to_private_dict() if p.player_id == viewer_id else p.to_public_dict()
                for p in self.players
            ],
            "top_card": top_card.to_dict() if top_card else None,
            "current_color": self.current_color,
            "current_player_id": current.player_id if current else None,
            "direction": self.turn_manager.get_direction_text(),
            "pending_penalty": self.pending_penalty,
            "winner": self.winner,
            "started": self.started,
        }
