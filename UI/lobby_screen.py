import pygame
import UI.theme as _t
from UI.theme import BG, PANEL_BG, PANEL_EDGE, TEXT_LIGHT, TEXT_MUTED, BTN_BG, BTN_HOVER, BTN_BORDER, W, H


class LobbyScreen:
    def __init__(self, client):
        self.client = client
        self.room_code = ""
        self.players = []
        self.is_host = False

        cx = W // 2
        self._start_btn = pygame.Rect(cx - 130, H - 150, 260, 48)
        self._leave_btn = pygame.Rect(cx - 130, H - 90,  260, 48)

    def set_room_data(self, room_code, players, is_host=False):
        self.room_code = room_code
        self.players = players
        self.is_host = is_host

    def render(self, surface):
        surface.fill(BG)

        title = _t.F_UI_LG.render("Waiting Room", True, TEXT_LIGHT)
        surface.blit(title, title.get_rect(centerx=W // 2, top=60))

        code_text = _t.F_UI.render(f"Room Code:  {self.room_code}", True, TEXT_MUTED)
        surface.blit(code_text, code_text.get_rect(centerx=W // 2, top=116))

        hint = _t.F_UI_SM.render("Share this code with your friends", True, TEXT_MUTED)
        surface.blit(hint, hint.get_rect(centerx=W // 2, top=142))

        # Player list panel
        panel = pygame.Rect(W // 2 - 210, 170, 420, 300)
        pygame.draw.rect(surface, PANEL_BG, panel, border_radius=10)
        pygame.draw.rect(surface, PANEL_EDGE, panel, 1, border_radius=10)

        for i, player in enumerate(self.players):
            name = player.get("name", player.get("player_name", "Unknown"))
            is_host = player.get("is_host", False)
            tag = "  [Host]" if is_host else ""
            connected = player.get("connected", True)
            color = TEXT_MUTED if not connected else TEXT_LIGHT
            lbl = _t.F_UI.render(f"{i + 1}.  {name}{tag}", True, color)
            surface.blit(lbl, (panel.x + 24, panel.y + 20 + i * 52))

        waiting = _t.F_UI_SM.render(
            f"{len(self.players)}/4 players  —  waiting for host to start...",
            True, TEXT_MUTED,
        )
        if not self.is_host:
            surface.blit(waiting, waiting.get_rect(centerx=W // 2, top=panel.bottom + 16))

        # Buttons
        mouse = pygame.mouse.get_pos()
        if self.is_host:
            c = BTN_HOVER if self._start_btn.collidepoint(mouse) else BTN_BG
            pygame.draw.rect(surface, c, self._start_btn, border_radius=8)
            pygame.draw.rect(surface, BTN_BORDER, self._start_btn, 1, border_radius=8)
            start_lbl = _t.F_UI.render("Start Game", True, TEXT_LIGHT)
            surface.blit(start_lbl, start_lbl.get_rect(center=self._start_btn.center))

        lc = BTN_HOVER if self._leave_btn.collidepoint(mouse) else BTN_BG
        pygame.draw.rect(surface, lc, self._leave_btn, border_radius=8)
        pygame.draw.rect(surface, BTN_BORDER, self._leave_btn, 1, border_radius=8)
        leave_lbl = _t.F_UI.render("Leave Room", True, TEXT_LIGHT)
        surface.blit(leave_lbl, leave_lbl.get_rect(center=self._leave_btn.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_host and self._start_btn.collidepoint(event.pos):
                try:
                    self.client.start_game()
                except Exception:
                    pass
                return "START_GAME"
            if self._leave_btn.collidepoint(event.pos):
                try:
                    self.client.leave_room()
                except Exception:
                    pass
                return "LEAVE_ROOM"
        return None
