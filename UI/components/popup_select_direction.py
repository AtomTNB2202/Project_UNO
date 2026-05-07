"""
Direction Selection Popup — shown when player plays a 0 card.
Player chooses which direction hands are passed (CW or CCW).
"""

import pygame
import UI.theme as _t
from UI.theme import (
    DIR_CW, DIR_CCW,
    PANEL_BG, PANEL_EDGE, TEXT_LIGHT, WHITE,
    W, H)

_OPTIONS = [
    ("CLOCKWISE",         "R",  DIR_CW),
    ("COUNTER_CLOCKWISE", "L",  DIR_CCW),
]

_BTN_W, _BTN_H = 160, 90
_GAP = 30
_TOTAL_W = _BTN_W * 2 + _GAP
_PANEL_W = _TOTAL_W + 80
_PANEL_H = 210


class PopupSelectDirection:
    def __init__(self):
        self.visible = False
        self._buttons = []   # list of (pygame.Rect, value, label, color)

    def show(self):
        self.visible = True
        self._build_buttons()

    def hide(self):
        self.visible = False

    def render(self, surface):
        if not self.visible:
            return

        dim = pygame.Surface((W, H), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 160))
        surface.blit(dim, (0, 0))

        px = W // 2 - _PANEL_W // 2
        py = H // 2 - _PANEL_H // 2
        panel = pygame.Rect(px, py, _PANEL_W, _PANEL_H)
        pygame.draw.rect(surface, PANEL_BG, panel, border_radius=14)
        pygame.draw.rect(surface, PANEL_EDGE, panel, 2, border_radius=14)

        title = _t.F_UI_LG.render("Chon huong truyen bai", True, TEXT_LIGHT)
        surface.blit(title, title.get_rect(centerx=W // 2, top=py + 18))

        mouse_pos = pygame.mouse.get_pos()
        for rect, value, label, color in self._buttons:
            is_hover = rect.collidepoint(mouse_pos)
            if is_hover:
                grow = pygame.Rect(rect.x - 4, rect.y - 4, rect.w + 8, rect.h + 8)
                pygame.draw.rect(surface, color, grow, border_radius=12)
                pygame.draw.rect(surface, WHITE, grow, 3, border_radius=12)
            else:
                pygame.draw.rect(surface, color, rect, border_radius=10)
                pygame.draw.rect(surface, (200, 200, 200), rect, 2, border_radius=10)
            lbl = _t.F_UI_LG.render(label, True, WHITE)
            surface.blit(lbl, lbl.get_rect(center=rect.center))

    def handle_event(self, event):
        """Returns direction string ('CLOCKWISE' or 'COUNTER_CLOCKWISE'), or None."""
        if not self.visible:
            return None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, value, label, color in self._buttons:
                if rect.collidepoint(event.pos):
                    self.hide()
                    return value
        return None

    def _build_buttons(self):
        self._buttons = []
        py = H // 2 - _PANEL_H // 2
        start_x = W // 2 - _TOTAL_W // 2
        btn_y = py + 90
        for i, (value, label, color) in enumerate(_OPTIONS):
            rect = pygame.Rect(start_x + i * (_BTN_W + _GAP), btn_y, _BTN_W, _BTN_H)
            self._buttons.append((rect, value, label, color))
