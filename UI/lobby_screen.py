import pygame
import UI.theme as _t
from UI.theme import (
    BG, PANEL_BG, PANEL_EDGE,
    TEXT_LIGHT, TEXT_MUTED,
    BTN_BG, BTN_HOVER, BTN_BORDER,
    W, H)

_ON_COLOR  = (50, 160, 80)
_OFF_COLOR = (80, 80, 90)
_TOGGLE_W, _TOGGLE_H = 58, 28

_RULES = [
    ("rule_0", "Rule 0  —  Pass Hands"),
    ("rule_7", "Rule 7  —  Swap Hands"),
    ("rule_8", "Rule 8  —  Reaction"),
]


class LobbyScreen:
    def __init__(self, client):
        self.client = client
        self.room_code = ""
        self.players = []
        self.is_host = False
        self._error = ""

        # House-rule settings (host controls, guests see them but cannot change)
        self.settings = {"rule_0": True, "rule_7": True, "rule_8": True}

        cx = W // 2
        self._start_btn = pygame.Rect(cx - 130, H - 150, 260, 48)
        self._leave_btn = pygame.Rect(cx - 130, H - 90,  260, 48)

        # Settings panel (right of player list)
        self._settings_panel = pygame.Rect(W // 2 + 230, 170, 280, 180)
        self._toggle_rects = {}   # key -> pygame.Rect (built in _build_toggles)
        self._build_toggles()

    def _build_toggles(self):
        px = self._settings_panel.x + self._settings_panel.w - _TOGGLE_W - 14
        py_start = self._settings_panel.y + 44
        for i, (key, _) in enumerate(_RULES):
            self._toggle_rects[key] = pygame.Rect(px, py_start + i * 48, _TOGGLE_W, _TOGGLE_H)

    def set_room_data(self, room_code, players, is_host=False, settings=None):
        self.room_code = room_code
        self.players = players
        self.is_host = is_host
        if len(self.players) >= 2:
            self._error = ""
        # Non-host always takes settings from server; host keeps local state
        # (server echoes them back immediately after each toggle)
        if settings is not None:
            self.settings.update(settings)

    def set_error(self, message):
        self._error = message or ""

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

        # House rules settings panel (always visible, host can toggle)
        self._render_settings(surface)

        # Buttons
        mouse = pygame.mouse.get_pos()
        if self.is_host:
            can_start = len(self.players) >= 2
            if can_start:
                c = BTN_HOVER if self._start_btn.collidepoint(mouse) else BTN_BG
            else:
                c = (55, 58, 68)
            pygame.draw.rect(surface, c, self._start_btn, border_radius=8)
            pygame.draw.rect(surface, BTN_BORDER, self._start_btn, 1, border_radius=8)
            start_color = TEXT_LIGHT if can_start else TEXT_MUTED
            start_lbl = _t.F_UI.render("Start Game", True, start_color)
            surface.blit(start_lbl, start_lbl.get_rect(center=self._start_btn.center))
            if not can_start and not self._error:
                hint = _t.F_UI_SM.render("Need at least 2 players to start.", True, TEXT_MUTED)
                surface.blit(hint, hint.get_rect(centerx=W // 2, top=self._start_btn.bottom + 8))

        lc = BTN_HOVER if self._leave_btn.collidepoint(mouse) else BTN_BG
        pygame.draw.rect(surface, lc, self._leave_btn, border_radius=8)
        pygame.draw.rect(surface, BTN_BORDER, self._leave_btn, 1, border_radius=8)
        leave_lbl = _t.F_UI.render("Leave Room", True, TEXT_LIGHT)
        surface.blit(leave_lbl, leave_lbl.get_rect(center=self._leave_btn.center))

        if self._error:
            err = _t.F_UI_SM.render(self._error, True, (220, 80, 80))
            surface.blit(err, err.get_rect(centerx=W // 2, top=self._start_btn.bottom + 8))

    def _render_settings(self, surface):
        sp = self._settings_panel
        pygame.draw.rect(surface, PANEL_BG, sp, border_radius=10)
        pygame.draw.rect(surface, PANEL_EDGE, sp, 1, border_radius=10)

        hdr = _t.F_UI.render("House Rules", True, TEXT_LIGHT)
        surface.blit(hdr, (sp.x + 14, sp.y + 12))

        host_note = "(host only)" if not self.is_host else ""
        note_s = _t.F_UI_SM.render(host_note, True, TEXT_MUTED)
        surface.blit(note_s, (sp.x + 14, sp.y + 32))

        for key, label in _RULES:
            rect = self._toggle_rects[key]
            row_y = rect.y + (_TOGGLE_H - 17) // 2
            lbl_s = _t.F_UI_SM.render(label, True, TEXT_LIGHT)
            surface.blit(lbl_s, (sp.x + 14, row_y))

            enabled = self.settings.get(key, True)
            bg = _ON_COLOR if enabled else _OFF_COLOR
            pygame.draw.rect(surface, bg, rect, border_radius=6)
            text = "ON" if enabled else "OFF"
            t_surf = _t.F_UI_SM.render(text, True, (255, 255, 255))
            surface.blit(t_surf, t_surf.get_rect(center=rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Toggle buttons (host only)
            if self.is_host:
                for key, rect in self._toggle_rects.items():
                    if rect.collidepoint(event.pos):
                        self.settings[key] = not self.settings.get(key, True)
                        try:
                            self.client.send_settings(self.settings)
                        except Exception:
                            pass
                        return None

            if self.is_host and self._start_btn.collidepoint(event.pos):
                if len(self.players) < 2:
                    self._error = "Need at least 2 players to start."
                    return None
                try:
                    self.client.start_game(settings=self.settings)
                    self._error = ""
                except Exception as exc:
                    self._error = str(exc)
                    return None
                return None

            if self._leave_btn.collidepoint(event.pos):
                try:
                    self.client.leave_room()
                except Exception:
                    pass
                return "LEAVE_ROOM"
        return None
