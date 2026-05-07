""" Status Panel — thin bar at the top showing turn, color, direction, penalty. """

import pygame
import UI.theme as _t
from UI.theme import (
    PANEL_BG,
    PANEL_EDGE,
    CARD_COLORS,
    TEXT_LIGHT,
    TEXT_MUTED,
    WARNING,
    DIR_CW,
    DIR_CCW,
    W,
    STATUS_H,
)
from UI.components.card_component import CardComponent


class StatusPanel:
    def __init__(self):
        self.current_player_id = None
        self.current_player_name = "Player"
        self.current_color = None
        self.direction = "CLOCKWISE"
        self.pending_penalty = 0
        self.top_card = None
        self.is_my_turn = False
        self._top_card_comp = None

    def set_state(self, game_state, my_id):
        self.current_player_id = game_state.get("current_player_id")

        players = game_state.get("players", [])
        current_player = next(
            (p for p in players if p.get("player_id") == self.current_player_id),
            None,
        )

        if current_player:
            self.current_player_name = current_player.get("name", "Player")
        else:
            self.current_player_name = "Unknown Player"

        self.current_color = game_state.get("current_color")
        self.direction = game_state.get("direction", "CLOCKWISE")
        self.pending_penalty = game_state.get("pending_penalty", 0)

        self.is_my_turn = self.current_player_id == my_id

        top = game_state.get("top_card")
        if top:
            self._top_card_comp = CardComponent(top, (0, 0), (46, 66))
        else:
            self._top_card_comp = None

    def render(self, surface):
        # Background bar
        bar = pygame.Rect(0, 0, W, STATUS_H)
        pygame.draw.rect(surface, PANEL_BG, bar)
        pygame.draw.line(surface, PANEL_EDGE, (0, STATUS_H), (W, STATUS_H), 1)

        x = 14

        # Turn indicator
        if self.is_my_turn:
            turn_label = "YOUR TURN"
            turn_color = (80, 220, 120)
        else:
            turn_label = f"{self.current_player_name}'s turn"
            turn_color = TEXT_LIGHT

        _blit(surface, _t.F_UI, turn_label, turn_color, x, STATUS_H // 2)
        x += 260

        # Current active colour swatch
        if self.current_color:
            swatch_c = CARD_COLORS.get(self.current_color, (80, 80, 80))
            pygame.draw.circle(surface, swatch_c, (x + 10, STATUS_H // 2), 11)
            pygame.draw.circle(surface, (200, 200, 200), (x + 10, STATUS_H // 2), 11, 2)
            _blit(surface, _t.F_UI_SM, self.current_color, TEXT_MUTED, x + 26, STATUS_H // 2)
            x += 130

        # Direction arrow
        dir_color = DIR_CW if self.direction == "CLOCKWISE" else DIR_CCW
        dir_sym = "↻ CW" if self.direction == "CLOCKWISE" else "↺ CCW"
        _blit(surface, _t.F_UI, dir_sym, dir_color, x, STATUS_H // 2)
        x += 110

        # Pending penalty badge
        if self.pending_penalty > 0:
            badge = f"+{self.pending_penalty} PENDING"
            _blit(surface, _t.F_UI, badge, WARNING, x, STATUS_H // 2)

        # Mini top card on the right
        if self._top_card_comp:
            self._top_card_comp.pos = [W - 60, (STATUS_H - 66) // 2]
            self._top_card_comp.render(surface)


def _blit(surface, font, text, color, x, cy):
    surf = font.render(str(text), True, color)
    surface.blit(surf, (x, cy - surf.get_height() // 2))