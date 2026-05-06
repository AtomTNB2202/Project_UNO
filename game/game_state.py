from game.card import Color, CardType
from game.deck import Deck
from game.player import Player
from game.turn_manager import TurnManager
from game.rule_engine import RuleEngine
from game.custom_rules.rule_zero import RuleZero
from game.custom_rules.rule_seven import RuleSeven
from game.custom_rules.rule_eight import RuleEight
from game.custom_rules.stacking_rule import StackingRule
from config import MAX_PLAYERS, MIN_PLAYERS, INITIAL_HAND_SIZE, REACTION_TIME_LIMIT


class GameState:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.turn_manager = TurnManager()
        self.started = False
        self.current_color = None
        self.pending_penalty = 0
        self.last_penalty_value = 0
        self.winner = None
        self.rule_eight = RuleEight()

    # ------------------------------------------------------------------
    # Player management (pre-game only)
    # ------------------------------------------------------------------

    def add_player(self, player_id, name):
        if self.started:
            raise RuntimeError("Cannot add players after the game has started.")
        if len(self.players) >= MAX_PLAYERS:
            raise RuntimeError(f"Room is full (max {MAX_PLAYERS} players).")
        self.players.append(Player(player_id, name))

    def remove_player(self, player_id):
        if self.started:
            raise RuntimeError("Cannot remove players after the game has started.")
        self.players = [p for p in self.players if p.player_id != player_id]

    def can_start(self):
        return MIN_PLAYERS <= len(self.players) <= MAX_PLAYERS

    # ------------------------------------------------------------------
    # Game start
    # ------------------------------------------------------------------

    def start_game(self):
        if not self.can_start():
            raise RuntimeError(
                f"Need between {MIN_PLAYERS} and {MAX_PLAYERS} players to start."
            )
        self.deck.build_standard_deck()
        self.deck.shuffle()

        for player in self.players:
            player.add_cards(self.deck.draw_many(INITIAL_HAND_SIZE))

        # Draw first discard card; skip wild cards (standard rule).
        first_card = self.deck.draw_one()
        while first_card is not None and first_card.is_wild_card():
            self.deck.put_to_discard(first_card)
            first_card = self.deck.draw_one()

        self.deck.put_to_discard(first_card)
        self.current_color = first_card.color
        self.started = True

    # ------------------------------------------------------------------
    # Turn helpers
    # ------------------------------------------------------------------

    def get_current_player(self):
        return self.players[self.turn_manager.current_player_index()]

    def find_player_index(self, player_id):
        for i, p in enumerate(self.players):
            if p.player_id == player_id:
                return i
        return -1

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
            raise RuntimeError("The game has not started yet.")
        if self.get_current_player().player_id != player_id:
            raise RuntimeError("It is not your turn.")

        player_idx = self.find_player_index(player_id)
        player = self.players[player_idx]

        if card_index < 0 or card_index >= player.card_count():
            raise IndexError(f"Card index {card_index} is out of range.")

        card = player.hand[card_index]
        top_card = self.deck.top_discard()

        if not RuleEngine.is_legal_card(
            card, top_card, self.current_color,
            self.pending_penalty, self.last_penalty_value
        ):
            raise ValueError("That card cannot be played right now.")

        # No-win-with-action-card rule: final card must be a number.
        if player.card_count() == 1 and not RuleEngine.can_play_as_final_card(card):
            raise ValueError("You cannot win with an action or wild card.")

        # Wild cards require a chosen color.
        if card.is_wild_card() and not chosen_color:
            raise ValueError("You must choose a color when playing a Wild card.")

        # Commit the play.
        played_card = player.remove_card(card_index)
        self.deck.put_to_discard(played_card)

        # Update current color.
        if played_card.is_wild_card():
            self.current_color = Color(chosen_color)
        else:
            self.current_color = played_card.color

        # Apply the card's effect (also advances the turn internally).
        effect_result = self.apply_card_effect(
            played_card, player_id, chosen_color, zero_direction, seven_target_id
        )

        # Check for winner.
        if player.has_no_cards():
            self.winner = player_id
            return {
                "action": "play",
                "card": repr(played_card),
                "winner": player_id,
                "effect": effect_result,
            }

        return {"action": "play", "card": repr(played_card), "effect": effect_result}

    def draw_card(self, player_id):
        if not self.started:
            raise RuntimeError("The game has not started yet.")
        if self.get_current_player().player_id != player_id:
            raise RuntimeError("It is not your turn.")

        player = self.players[self.find_player_index(player_id)]

        if self.pending_penalty > 0:
            result = StackingRule.resolve_penalty(player, self.deck, self.pending_penalty)
            state = StackingRule.reset_penalty_state()
            self.pending_penalty = state["pending_penalty"]
            self.last_penalty_value = state["last_penalty_value"]
            self.turn_manager.next_turn(len(self.players))
            return {"action": "draw_penalty", **result}

        card = self.deck.draw_one()
        player.add_card(card)
        self.turn_manager.next_turn(len(self.players))
        return {"action": "draw", "card": repr(card)}

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
        result = {}

        if card.card_type == CardType.SKIP:
            self.turn_manager.skip_next(n)
            result["effect"] = "skip"

        elif card.card_type == CardType.REVERSE:
            self.turn_manager.reverse_direction(n)
            # For 2-player, reverse_direction already repositioned the index
            # so that the current player goes again; skip calling next_turn.
            # For 3-4 players, advance normally in the reversed direction.
            if n > 2:
                self.turn_manager.next_turn(n)
            result["effect"] = "reverse"
            result["direction"] = self.turn_manager.get_direction_text()

        elif card.card_type == CardType.DRAW_TWO:
            self.pending_penalty = StackingRule.add_penalty(self.pending_penalty, card)
            self.last_penalty_value = 2
            self.turn_manager.next_turn(n)
            result["effect"] = "draw_two"
            result["pending_penalty"] = self.pending_penalty

        elif card.card_type == CardType.WILD:
            self.turn_manager.next_turn(n)
            result["effect"] = "wild"
            result["chosen_color"] = chosen_color

        elif card.card_type == CardType.WILD_DRAW_FOUR:
            self.pending_penalty = StackingRule.add_penalty(self.pending_penalty, card)
            self.last_penalty_value = 4
            self.turn_manager.next_turn(n)
            result["effect"] = "wild_draw_four"
            result["pending_penalty"] = self.pending_penalty

        elif card.card_type == CardType.NUMBER:
            if card.value == 0 and zero_direction:
                rule_result = self.apply_rule_zero(zero_direction)
                result["effect"] = "rule_zero"
                result.update(rule_result)
            elif card.value == 7 and seven_target_id:
                rule_result = self.apply_rule_seven(player_id, seven_target_id)
                result["effect"] = "rule_seven"
                result.update(rule_result)
            elif card.value == 8:
                rule_result = self.start_reaction_event(player_id)
                result["effect"] = "rule_eight"
                result.update(rule_result)
            else:
                result["effect"] = "number"
            self.turn_manager.next_turn(n)

        return result

    # ------------------------------------------------------------------
    # Custom rule delegates
    # ------------------------------------------------------------------

    def apply_rule_zero(self, direction):
        RuleZero.validate_direction(direction)
        return RuleZero.apply(self.players, direction)

    def apply_rule_seven(self, player_id, target_player_id):
        return RuleSeven.apply(self.players, player_id, target_player_id)

    def start_reaction_event(self, player_id):
        return self.rule_eight.start_event(self.players, REACTION_TIME_LIMIT)

    def submit_reaction(self, player_id):
        return self.rule_eight.submit_response(player_id)

    def finish_reaction_event(self):
        return self.rule_eight.finish_event(self.players, self.deck)

    # ------------------------------------------------------------------
    # State serialisation
    # ------------------------------------------------------------------

    def to_dict_for_player(self, viewer_id):
        current_player_id = (
            self.get_current_player().player_id if self.started and self.players else None
        )
        top_card = self.deck.top_discard()
        players_data = []
        for p in self.players:
            if p.player_id == viewer_id:
                players_data.append(p.to_private_dict())
            else:
                players_data.append(p.to_public_dict())

        return {
            "started": self.started,
            "current_player": current_player_id,
            "current_color": self.current_color.value if self.current_color else None,
            "top_card": top_card.to_dict() if top_card else None,
            "direction": self.turn_manager.get_direction_text(),
            "pending_penalty": self.pending_penalty,
            "winner": self.winner,
            "reaction_active": self.rule_eight.active,
            "players": players_data,
        }
