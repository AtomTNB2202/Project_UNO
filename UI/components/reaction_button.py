"""
Reaction Button — large centre button for Rule of 8.
Shows a circular countdown arc that drains as time runs out.
"""

import pygame
import UI.theme as _t
import time
import math
import random
from UI.theme import (
    BG, PANEL_BG, PANEL_EDGE,
    REACTION_BG, REACTION_DONE, WHITE, TEXT_LIGHT, TEXT_MUTED, WARNING,
    W, H)

_BTN_R = 72     # button radius
_MARGIN = _BTN_R + 34


class ReactionButton:
    def __init__(self):
        self.visible = False
        self.clicked = False
        self._start_time = None
        self._window = 3        # seconds, updated from event data
        self._cx = W // 2
        self._cy = H // 2

    def show(self, response_window=3):
        self.visible = True
        self.clicked = False
        self._start_time = time.time()
        self._window = response_window
        self._randomize_position()

    def hide(self):
        self.visible = False

    def render(self, surface):
        if not self.visible:
            return

        elapsed = time.time() - self._start_time if self._start_time else 0
        remaining = max(0.0, self._window - elapsed)
        frac = remaining / self._window  # 1.0 → 0.0

        # Full-screen reaction overlay
        dim = pygame.Surface((W, H), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 185))
        surface.blit(dim, (0, 0))

        banner = pygame.Rect(W // 2 - 280, 28, 560, 86)
        pygame.draw.rect(surface, PANEL_BG, banner, border_radius=10)
        pygame.draw.rect(surface, PANEL_EDGE, banner, 1, border_radius=10)
        title = _t.F_UI_LG.render("Rule 8 Reaction!", True, WHITE)
        surface.blit(title, title.get_rect(centerx=banner.centerx, top=banner.y + 14))
        help_text = _t.F_UI.render("Click the random button before time runs out", True, TEXT_MUTED)
        surface.blit(help_text, help_text.get_rect(centerx=banner.centerx, top=banner.y + 52))

        cx, cy = self._cx, self._cy

        # Background circle
        circle_color = REACTION_DONE if self.clicked else REACTION_BG
        pygame.draw.circle(surface, (*BG, 150), (cx + 5, cy + 7), _BTN_R + 3)
        pygame.draw.circle(surface, circle_color, (cx, cy), _BTN_R)
        pygame.draw.circle(surface, WHITE, (cx, cy), _BTN_R, 3)

        # Countdown arc (white, drains clockwise from top)
        if not self.clicked and frac > 0:
            _draw_arc(surface, cx, cy, _BTN_R + 10, frac)

        # Label
        if self.clicked:
            label = _t.F_UI_LG.render("OK! READY", True, WHITE)
        else:
            label = _t.F_UI_LG.render("REACT!", True, WHITE)
        surface.blit(label, label.get_rect(center=(cx, cy - 8)))

        # Countdown seconds text
        if not self.clicked:
            sec_color = TEXT_LIGHT if remaining > 1 else WARNING
            sec_txt = _t.F_UI.render(f"{remaining:.1f}s", True, sec_color)
            surface.blit(sec_txt, sec_txt.get_rect(center=(cx, cy + 22)))

    def handle_event(self, event):
        """Returns True the moment the player clicks and hasn't clicked yet."""
        if not self.visible or self.clicked:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dx = event.pos[0] - self._cx
            dy = event.pos[1] - self._cy
            if math.hypot(dx, dy) <= _BTN_R:
                self.clicked = True
                return True
        return False

    def _randomize_position(self):
        self._cx = random.randint(_MARGIN, W - _MARGIN)
        self._cy = random.randint(150 + _BTN_R, H - _MARGIN)


def _draw_arc(surface, cx, cy, r, frac):
    """Draw a clockwise-draining arc from top, frac 1.0=full → 0.0=empty."""
    steps = 64
    angle_start = -math.pi / 2                  # 12 o'clock
    angle_end   = angle_start + 2 * math.pi * frac
    pts = [(cx, cy)]
    for i in range(steps + 1):
        a = angle_start + (angle_end - angle_start) * i / steps
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    if len(pts) >= 3:
        pygame.draw.polygon(surface, (*WHITE, 60), pts)
