import pygame
import UI.theme as _t
from UI.theme import BG, TEXT_LIGHT, TEXT_MUTED, BTN_BG, BTN_HOVER, BTN_BORDER, W, H


class MainMenu:
    def __init__(self):
        btn_w, btn_h = 280, 52
        cx = W // 2
        self._buttons = {
            "CREATE_ROOM": pygame.Rect(cx - btn_w // 2, H // 2 - 105, btn_w, btn_h),
            "JOIN_ROOM":   pygame.Rect(cx - btn_w // 2, H // 2 - 35,  btn_w, btn_h),
            "RULES":       pygame.Rect(cx - btn_w // 2, H // 2 + 35,  btn_w, btn_h),
            "QUIT":        pygame.Rect(cx - btn_w // 2, H // 2 + 105, btn_w, btn_h),
        }
        self._labels = {
            "CREATE_ROOM": "Create Room",
            "JOIN_ROOM":   "Join Room",
            "RULES":       "How to Play",
            "QUIT":        "Quit",
        }

    def render(self, surface):
        surface.fill(BG)

        title = _t.F_UI_LG.render("Custom UNO Online", True, TEXT_LIGHT)
        surface.blit(title, title.get_rect(centerx=W // 2, top=H // 4))

        sub = _t.F_UI.render("Select an option to get started", True, TEXT_MUTED)
        surface.blit(sub, sub.get_rect(centerx=W // 2, top=H // 4 + 44))

        mouse = pygame.mouse.get_pos()
        for action, rect in self._buttons.items():
            color = BTN_HOVER if rect.collidepoint(mouse) else BTN_BG
            pygame.draw.rect(surface, color, rect, border_radius=8)
            pygame.draw.rect(surface, BTN_BORDER, rect, 1, border_radius=8)
            lbl = _t.F_UI.render(self._labels[action], True, TEXT_LIGHT)
            surface.blit(lbl, lbl.get_rect(center=rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for action, rect in self._buttons.items():
                if rect.collidepoint(event.pos):
                    return action
        return None
