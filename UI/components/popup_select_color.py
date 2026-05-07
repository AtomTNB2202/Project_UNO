"""
Color Selection Popup — shown when player plays Wild or Wild Draw Four.
"""

import pygame
import UI.theme as _t
from UI.theme import (
    CARD_COLORS, CARD_RED, CARD_GREEN, CARD_BLUE, CARD_YELLOW,
    PANEL_BG, PANEL_EDGE, TEXT_LIGHT, WHITE,
    W, H)

_COLORS = [
    ("RED",    CARD_RED),
    ("GREEN",  CARD_GREEN),
    ("BLUE",   CARD_BLUE),
    ("YELLOW", CARD_YELLOW),
]

_BTN_W, _BTN_H = 100, 100
_GAP = 18
_TOTAL_W = _BTN_W * 4 + _GAP * 3
_PANEL_W = _TOTAL_W + 80
_PANEL_H = 200


class PopupSelectColor:
    def __init__(self):
        self.visible = False
        self._buttons = []          # list of (pygame.Rect, color_name, color_rgb)
        self._hovered = None

    def show(self):
        self.visible = True
        self._build_buttons()

    def hide(self):
        self.visible = False

    def render(self, surface):
        if not self.visible:
            return

        # Dim overlay
        dim = pygame.Surface((W, H), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 160))
        surface.blit(dim, (0, 0))

        # Panel
        px = W // 2 - _PANEL_W // 2
        py = H // 2 - _PANEL_H // 2
        panel = pygame.Rect(px, py, _PANEL_W, _PANEL_H)
        pygame.draw.rect(surface, PANEL_BG, panel, border_radius=14)
        pygame.draw.rect(surface, PANEL_EDGE, panel, 2, border_radius=14)

        # Title
        title = _t.F_UI_LG.render("Choose a colour", True, TEXT_LIGHT)
        surface.blit(title, title.get_rect(centerx=W // 2, top=py + 18))

        # Colour buttons
        mouse_pos = pygame.mouse.get_pos()
        for rect, name, rgb in self._buttons:
            is_hover = rect.collidepoint(mouse_pos)
            br = 10
            if is_hover:
                grow = pygame.Rect(rect.x - 4, rect.y - 4, rect.w + 8, rect.h + 8)
                pygame.draw.rect(surface, rgb, grow, border_radius=br + 3)
                pygame.draw.rect(surface, WHITE, grow, 3, border_radius=br + 3)
            else:
                pygame.draw.rect(surface, rgb, rect, border_radius=br)
                pygame.draw.rect(surface, (200, 200, 200), rect, 2, border_radius=br)
            label = _t.F_UI.render(name, True, WHITE)
            surface.blit(label, label.get_rect(centerx=rect.centerx, top=rect.bottom + 5))

    def handle_event(self, event):
        """Returns chosen color string, or None."""
        if not self.visible:
            return None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, name, _ in self._buttons:
                if rect.collidepoint(event.pos):
                    self.hide()
                    return name
        return None

    def _build_buttons(self):
        self._buttons = []
        py = H // 2 - _PANEL_H // 2
        start_x = W // 2 - _TOTAL_W // 2
        btn_y = py + 70
        for i, (name, rgb) in enumerate(_COLORS):
            rect = pygame.Rect(start_x + i * (_BTN_W + _GAP), btn_y, _BTN_W, _BTN_H)
            self._buttons.append((rect, name, rgb))
