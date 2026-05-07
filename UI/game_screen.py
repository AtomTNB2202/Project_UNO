"""
Game Screen — main gameplay view.
"""

import pygame
import UI.theme as _t
from UI.theme import (
    BG, TABLE, PANEL_BG, PANEL_EDGE, CARD_COLORS,
    TEXT_MUTED, WHITE,
    PLAY_CX, PLAY_CY, STATUS_H, OPP_STRIP_H,
    CARD_W, CARD_H)
from UI.components.card_component import CardComponent, draw_card_back
from UI.components.hand_view import HandView
from UI.components.opponent_panel import OpponentPanel
from UI.components.status_panel import StatusPanel
from UI.components.popup_select_color import PopupSelectColor
from UI.components.popup_select_target import PopupSelectTarget
from UI.components.reaction_button import ReactionButton
from UI.components.result_screen import ResultScreen


class GameScreen:
    def __init__(self, client):
        self.client = client
        self.my_id = getattr(client, "player_id", None)
        self.game_state = {}

        self.hand_view      = HandView()
        self.opp_panel      = OpponentPanel()
        self.status_panel   = StatusPanel()
        self.popup_color    = PopupSelectColor()
        self.popup_target   = PopupSelectTarget()
        self.reaction_btn   = ReactionButton()
        self.result_screen  = ResultScreen()

        # Draw-pile button
        _bw, _bh = 94, 136
        self._draw_btn = pygame.Rect(PLAY_CX - 140 - _bw // 2, PLAY_CY - _bh // 2, _bw, _bh)

        self._selected_card_index = None
        self._pending_card_type   = None    # "wild" | "zero" | "seven" | None

    # ------------------------------------------------------------------
    def set_game_state(self, state):
        self.game_state = state
        if not state:
            return

        my_data = next((p for p in state["players"] if p["player_id"] == self.my_id), None)
        hand = my_data.get("hand", []) if my_data else []
        self.hand_view.set_cards(hand)

        opponents = [p for p in state["players"] if p["player_id"] != self.my_id]
        self.opp_panel.set_opponents(opponents)
        self.status_panel.set_state(state, self.my_id)

        if state.get("winner"):
            self.result_screen.set_result(state["winner"], state["players"], self.my_id)

    # ------------------------------------------------------------------
    def render(self, surface):
        surface.fill(BG)

        # Felt play area
        felt = pygame.Rect(PLAY_CX - 310, STATUS_H + OPP_STRIP_H + 20, 620, 280)
        pygame.draw.rect(surface, TABLE, felt, border_radius=18)
        pygame.draw.rect(surface, PANEL_EDGE, felt, 1, border_radius=18)

        self._draw_piles(surface)
        self._draw_color_indicator(surface)
        self._draw_draw_button(surface)

        self.status_panel.render(surface)
        self.opp_panel.render(surface)
        self.hand_view.render(surface)

        # Popups (highest priority, drawn last)
        self.popup_color.render(surface)
        self.popup_target.render(surface)
        self.reaction_btn.render(surface)
        self.result_screen.render(surface)

    # ------------------------------------------------------------------
    def handle_event(self, event):
        # Result screen
        action = self.result_screen.handle_event(event)
        if action:
            return action   # "menu" or "quit" — let caller handle

        # Popups
        chosen_color = self.popup_color.handle_event(event)
        if chosen_color is not None:
            self._send_play(chosen_color=chosen_color)
            return None

        target_id = self.popup_target.handle_event(event)
        if target_id is not None:
            self._send_play(seven_target_id=target_id)
            return None

        # Reaction button
        if self.reaction_btn.handle_event(event):
            self.client.submit_reaction()
            return None

        # Draw button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._draw_btn.collidepoint(event.pos):
                self.request_draw_card()
                return None

        # Hand card click
        clicked_index = self.hand_view.handle_event(event)
        if clicked_index is not None:
            self._selected_card_index = clicked_index
            # Second click on same card = try to play
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._selected_card_index is not None:
                self.request_play_card(self._selected_card_index)

        return None

    # ------------------------------------------------------------------
    def request_play_card(self, card_index):
        my_data = next(
            (p for p in self.game_state.get("players", []) if p["player_id"] == self.my_id),
            None,
        )
        if not my_data:
            return
        hand = my_data.get("hand", [])
        if card_index >= len(hand):
            return

        card = hand[card_index]
        ctype = card["type"]
        cval  = card.get("value")

        self._pending_card_type = None

        if ctype in ("WILD", "WILD_DRAW_FOUR"):
            self._pending_card_type = "wild"
            self.popup_color.show()

        elif ctype == "NUMBER" and cval == 0:
            self._pending_card_type = "zero"
            self._show_direction_popup()

        elif ctype == "NUMBER" and cval == 7:
            self._pending_card_type = "seven"
            opponents = [p for p in self.game_state["players"] if p["player_id"] != self.my_id]
            self.popup_target.show(opponents)

        else:
            self.client.play_card(card_index)
            self.hand_view.clear_selection()
            self._selected_card_index = None

    def request_draw_card(self):
        self.client.draw_card()

    def handle_reaction_started(self, event_data):
        window = event_data.get("response_window", 3)
        self.reaction_btn.show(window)

    def handle_reaction_result(self, result_data):
        self.reaction_btn.hide()

    # ------------------------------------------------------------------
    def _send_play(self, chosen_color=None, zero_direction=None, seven_target_id=None):
        idx = self._selected_card_index
        if idx is None:
            return
        self.client.play_card(
            idx,
            chosen_color=chosen_color,
            zero_direction=zero_direction,
            seven_target_id=seven_target_id,
        )
        self.hand_view.clear_selection()
        self._selected_card_index = None

    def _show_direction_popup(self):
        """For Rule 0, reuse color popup with CW / CCW labels as a quick approach.
        The network team can replace this with a proper direction popup if desired."""
        # Quick-and-dirty: we'll show popup_color but interpret RED=CW, BLUE=CCW.
        # A dedicated DirectionPopup is cleaner — left for the UI sub-team.
        self.popup_color.show()

    def _draw_piles(self, surface):
        """Draw discard pile and draw pile in the centre of the felt."""
        top_card = self.game_state.get("top_card")

        # Discard pile (right of centre)
        dc_x = PLAY_CX + 50
        dc_y = PLAY_CY - CARD_H // 2
        if top_card:
            cc = CardComponent(top_card, (dc_x, dc_y), (CARD_W + 14, CARD_H + 20))
            cc.render(surface)
        else:
            _draw_placeholder(surface, dc_x, dc_y, CARD_W + 14, CARD_H + 20, "DISCARD")

        lbl = _t.F_UI_SM.render("Discard", True, TEXT_MUTED)
        surface.blit(lbl, lbl.get_rect(centerx=dc_x + (CARD_W + 14) // 2,
                                        top=dc_y + CARD_H + 24))

        # Draw pile (left of centre)
        dr_x = PLAY_CX - 50 - CARD_W - 14
        dr_y = dc_y
        draw_card_back(surface, dr_x, dr_y, CARD_W + 14, CARD_H + 20)
        lbl2 = _t.F_UI_SM.render("Draw pile", True, TEXT_MUTED)
        surface.blit(lbl2, lbl2.get_rect(centerx=dr_x + (CARD_W + 14) // 2,
                                          top=dr_y + CARD_H + 24))

        # Store draw pile rect for click detection
        self._draw_btn = pygame.Rect(dr_x, dr_y, CARD_W + 14, CARD_H + 20)

    def _draw_color_indicator(self, surface):
        """Circle showing the active colour, below the discard pile."""
        color_name = self.game_state.get("current_color")
        if not color_name:
            return
        rgb = CARD_COLORS.get(color_name, (80, 80, 80))
        cx = PLAY_CX + 50 + (CARD_W + 14) // 2
        cy = PLAY_CY + CARD_H // 2 + 46
        pygame.draw.circle(surface, rgb, (cx, cy), 10)
        pygame.draw.circle(surface, WHITE, (cx, cy), 10, 2)

    def _draw_draw_button(self, surface=None):
        """The clickable area is set to the draw pile card back rect in _draw_piles."""
        pass


def _draw_placeholder(surface, x, y, w, h, label):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, PANEL_BG, rect, border_radius=8)
    pygame.draw.rect(surface, PANEL_EDGE, rect, 1, border_radius=8)
    lbl = _t.F_UI_SM.render(label, True, TEXT_MUTED)
    surface.blit(lbl, lbl.get_rect(center=rect.center))
