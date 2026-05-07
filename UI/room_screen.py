import pygame
import UI.theme as _t
from UI.theme import BG, PANEL_BG, PANEL_EDGE, TEXT_LIGHT, TEXT_MUTED, BTN_BG, BTN_HOVER, BTN_BORDER, WHITE, W, H


class RoomScreen:
    def __init__(self, client):
        self.client = client
        self.player_name = ""
        self.room_code = ""
        self.mode = "CREATE"
        self._active_field = None
        self._error = ""

        cx = W // 2
        self._name_rect    = pygame.Rect(cx - 180, 260, 360, 44)
        self._code_rect    = pygame.Rect(cx - 180, 340, 360, 44)
        self._confirm_btn  = pygame.Rect(cx - 130, 430, 260, 48)
        self._back_btn     = pygame.Rect(cx - 130, 496, 260, 48)

    def set_mode(self, mode):
        self.mode = mode
        self.player_name = ""
        self.room_code = ""
        self._active_field = None
        self._error = ""

    def render(self, surface):
        surface.fill(BG)

        title = _t.F_UI_LG.render(
            "Create Room" if self.mode == "CREATE" else "Join Room",
            True, TEXT_LIGHT,
        )
        surface.blit(title, title.get_rect(centerx=W // 2, top=150))

        # Name field
        name_lbl = _t.F_UI_SM.render("Your Name", True, TEXT_MUTED)
        surface.blit(name_lbl, (self._name_rect.x, self._name_rect.y - 22))
        border = WHITE if self._active_field == "name" else PANEL_EDGE
        pygame.draw.rect(surface, PANEL_BG, self._name_rect, border_radius=6)
        pygame.draw.rect(surface, border, self._name_rect, 1, border_radius=6)
        surface.blit(
            _t.F_UI.render(self.player_name, True, TEXT_LIGHT),
            (self._name_rect.x + 10, self._name_rect.y + 12),
        )

        # Room code field (JOIN only)
        if self.mode == "JOIN":
            code_lbl = _t.F_UI_SM.render("Room Code", True, TEXT_MUTED)
            surface.blit(code_lbl, (self._code_rect.x, self._code_rect.y - 22))
            border2 = WHITE if self._active_field == "code" else PANEL_EDGE
            pygame.draw.rect(surface, PANEL_BG, self._code_rect, border_radius=6)
            pygame.draw.rect(surface, border2, self._code_rect, 1, border_radius=6)
            surface.blit(
                _t.F_UI.render(self.room_code.upper(), True, TEXT_LIGHT),
                (self._code_rect.x + 10, self._code_rect.y + 12),
            )

        # Error message
        if self._error:
            err = _t.F_UI_SM.render(self._error, True, (220, 80, 80))
            surface.blit(err, err.get_rect(centerx=W // 2, top=415))

        # Buttons
        mouse = pygame.mouse.get_pos()
        for rect, label in (
            (self._confirm_btn, "Confirm"),
            (self._back_btn, "Back"),
        ):
            color = BTN_HOVER if rect.collidepoint(mouse) else BTN_BG
            pygame.draw.rect(surface, color, rect, border_radius=8)
            pygame.draw.rect(surface, BTN_BORDER, rect, 1, border_radius=8)
            surface.blit(_t.F_UI.render(label, True, TEXT_LIGHT), _t.F_UI.render(label, True, TEXT_LIGHT).get_rect(center=rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._name_rect.collidepoint(event.pos):
                self._active_field = "name"
            elif self.mode == "JOIN" and self._code_rect.collidepoint(event.pos):
                self._active_field = "code"
            elif self._confirm_btn.collidepoint(event.pos):
                return self.submit()
            elif self._back_btn.collidepoint(event.pos):
                self._active_field = None
                return "BACK"
            else:
                self._active_field = None

        if event.type == pygame.KEYDOWN and self._active_field:
            if event.key == pygame.K_BACKSPACE:
                if self._active_field == "name":
                    self.player_name = self.player_name[:-1]
                else:
                    self.room_code = self.room_code[:-1]
            elif event.key == pygame.K_TAB:
                self._active_field = "code" if self._active_field == "name" else "name"
            elif event.key == pygame.K_RETURN:
                return self.submit()
            elif event.unicode.isprintable():
                if self._active_field == "name" and len(self.player_name) < 16:
                    self.player_name += event.unicode
                elif self._active_field == "code" and len(self.room_code) < 6:
                    self.room_code += event.unicode.upper()
        return None

    def submit(self):
        if not self.player_name.strip():
            self._error = "Please enter your name."
            return None
        if self.mode == "JOIN" and not self.room_code.strip():
            self._error = "Please enter a room code."
            return None
        self._error = ""
        try:
            if self.mode == "CREATE":
                self.client.create_room(self.player_name.strip())
            else:
                self.client.join_room(self.room_code.strip(), self.player_name.strip())
            return "SUBMITTED"
        except Exception as exc:
            self._error = str(exc)
            return None
