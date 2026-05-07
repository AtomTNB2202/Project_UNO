"""
Target Selection Popup — shown when player plays a 7 card.
"""

import pygame
import UI.theme as _t
from UI.theme import (
    PANEL_BG, PANEL_EDGE, BTN_BG, BTN_HOVER, BTN_BORDER,
    TEXT_LIGHT, TEXT_MUTED, WHITE,
    W, H)

_BTN_W, _BTN_H = 220, 52
_GAP = 12
_PANEL_W = 320


class PopupSelectTarget:
    def __init__(self):
        self.visible = False
        self._players = []
        self._buttons = []      # list of (rect, player_id, name)

    def show(self, players):
        """players: list of public dicts (excludes self)."""
        self.visible = True
        self._players = players
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
        panel_h = 80 + len(self._buttons) * (_BTN_H + _GAP) + 20
        px = W // 2 - _PANEL_W // 2
        py = H // 2 - panel_h // 2
        panel = pygame.Rect(px, py, _PANEL_W, panel_h)
        pygame.draw.rect(surface, PANEL_BG, panel, border_radius=14)
        pygame.draw.rect(surface, PANEL_EDGE, panel, 2, border_radius=14)

        title = _t.F_UI_LG.render("Swap hands with:", True, TEXT_LIGHT)
        surface.blit(title, title.get_rect(centerx=W // 2, top=py + 18))

        mouse_pos = pygame.mouse.get_pos()
        for rect, pid, name in self._buttons:
            hover = rect.collidepoint(mouse_pos)
            bg = BTN_HOVER if hover else BTN_BG
            pygame.draw.rect(surface, bg, rect, border_radius=8)
            pygame.draw.rect(surface, BTN_BORDER, rect, 1, border_radius=8)
            lbl = _t.F_UI.render(name, True, TEXT_LIGHT)
            surface.blit(lbl, lbl.get_rect(center=rect.center))

    def handle_event(self, event):
        """Returns target player_id string, or None."""
        if not self.visible:
            return None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, pid, _ in self._buttons:
                if rect.collidepoint(event.pos):
                    self.hide()
                    return pid
        return None

    def _build_buttons(self):
        self._buttons = []
        panel_h = 80 + len(self._players) * (_BTN_H + _GAP) + 20
        px = W // 2 - _PANEL_W // 2
        py = H // 2 - panel_h // 2
        bx = W // 2 - _BTN_W // 2
        for i, p in enumerate(self._players):
            by = py + 65 + i * (_BTN_H + _GAP)
            rect = pygame.Rect(bx, by, _BTN_W, _BTN_H)
            self._buttons.append((rect, p["player_id"], p["name"]))
