"""
Opponent Panel — shows each opponent's name and card count.
Up to 3 opponents arranged horizontally across the top area.
"""

import pygame
import UI.theme as _t
from UI.theme import (
    PANEL_BG, PANEL_EDGE, TEXT_LIGHT, TEXT_MUTED, WARNING,
    W, OPP_STRIP_Y, OPP_STRIP_H)
from UI.components.card_component import draw_card_back

_BACK_W, _BACK_H = 32, 46      # mini card back size


class OpponentPanel:
    def __init__(self):
        self.opponents = []     # list of public dicts

    def set_opponents(self, opponents):
        self.opponents = opponents

    def render(self, surface):
        n = len(self.opponents)
        if n == 0:
            return

        slot_w = min(340, (W - 40) // n)
        total_w = slot_w * n
        start_x = W // 2 - total_w // 2

        for i, opp in enumerate(self.opponents):
            x = start_x + i * slot_w + 8
            y = OPP_STRIP_Y
            w = slot_w - 16
            h = OPP_STRIP_H

            # Panel background
            panel = pygame.Rect(x, y, w, h)
            pygame.draw.rect(surface, PANEL_BG, panel, border_radius=8)
            pygame.draw.rect(surface, PANEL_EDGE, panel, 1, border_radius=8)

            # Mini card backs
            count = opp.get("card_count", 0)
            _draw_mini_hand(surface, x + 10, y + 36, count)

            # Name
            name = opp.get("name", "Player")
            name_surf = _t.F_UI.render(name, True, TEXT_LIGHT)
            surface.blit(name_surf, (x + 10, y + 8))

            # Card count badge
            badge_txt = _t.F_UI.render(f"{count}", True,
                                    WARNING if count <= 2 else TEXT_MUTED)
            surface.blit(badge_txt, (x + w - badge_txt.get_width() - 10, y + 8))


def _draw_mini_hand(surface, x, y, count):
    """Draw a short fan of mini card backs to represent an opponent's hand."""
    if count == 0:
        return
    show = min(count, 10)
    step = min(_BACK_W + 2, 18)
    for i in range(show):
        draw_card_back(surface, x + i * step, y, _BACK_W, _BACK_H)
