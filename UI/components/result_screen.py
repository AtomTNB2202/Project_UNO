"""
Result Screen — displayed when the game ends.
"""

import pygame
import UI.theme as _t
from UI.theme import (
    BG, PANEL_BG, PANEL_EDGE, BTN_BG, BTN_HOVER, BTN_BORDER,
    TEXT_LIGHT, TEXT_MUTED, GLOW_SELECT, WHITE,
    W, H)

_BTN_W, _BTN_H = 200, 50


class ResultScreen:
    def __init__(self):
        self.visible = False
        self.winner_name = ""
        self.is_winner = False
        self._btn_menu = None
        self._btn_quit = None

    def set_result(self, winner_id, players, my_id):
        self.visible = True
        winner = next((p for p in players if p["player_id"] == winner_id), None)
        self.winner_name = winner["name"] if winner else "Unknown"
        self.is_winner = (winner_id == my_id)
        self._build_buttons()

    def render(self, surface):
        if not self.visible:
            return

        # Full-screen dim
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        # Panel
        pw, ph = 480, 280
        px, py = W // 2 - pw // 2, H // 2 - ph // 2
        panel = pygame.Rect(px, py, pw, ph)
        pygame.draw.rect(surface, PANEL_BG, panel, border_radius=16)
        pygame.draw.rect(surface, PANEL_EDGE, panel, 2, border_radius=16)

        # Trophy line
        trophy = "🏆" if self.is_winner else "🃏"
        headline = f"{trophy}  {self.winner_name} wins!"
        hl_surf = _t.F_UI_LG.render(headline, True,
                                  GLOW_SELECT if self.is_winner else TEXT_LIGHT)
        surface.blit(hl_surf, hl_surf.get_rect(centerx=W // 2, top=py + 40))

        sub = "You won!" if self.is_winner else "Better luck next time."
        sub_surf = _t.F_UI.render(sub, True, TEXT_MUTED)
        surface.blit(sub_surf, sub_surf.get_rect(centerx=W // 2, top=py + 90))

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for rect, label in (self._btn_menu, self._btn_quit):
            bg = BTN_HOVER if rect.collidepoint(mouse_pos) else BTN_BG
            pygame.draw.rect(surface, bg, rect, border_radius=8)
            pygame.draw.rect(surface, BTN_BORDER, rect, 1, border_radius=8)
            lbl = _t.F_UI.render(label, True, TEXT_LIGHT)
            surface.blit(lbl, lbl.get_rect(center=rect.center))

    def handle_event(self, event):
        """Returns 'menu' or 'quit', or None."""
        if not self.visible:
            return None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._btn_menu and self._btn_menu[0].collidepoint(event.pos):
                return "menu"
            if self._btn_quit and self._btn_quit[0].collidepoint(event.pos):
                return "quit"
        return None

    def _build_buttons(self):
        cx, by = W // 2, H // 2 + 60
        self._btn_menu = (pygame.Rect(cx - _BTN_W - 10, by, _BTN_W, _BTN_H), "Back to Menu")
        self._btn_quit = (pygame.Rect(cx + 10,          by, _BTN_W, _BTN_H), "Quit")
