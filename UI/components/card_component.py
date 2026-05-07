"""
Card Component — draws one UNO card using only pygame primitives (no images).
"""

import pygame
import UI.theme as _t
from UI.theme import (
    CARD_COLORS, CARD_RED, CARD_GREEN, CARD_BLUE, CARD_YELLOW,
    WHITE, SHADOW, GLOW_SELECT,
    CARD_W, CARD_H, CARD_R)

_LABELS = {
    "SKIP": "SKIP",
    "REVERSE": "REV",
    "DRAW_TWO": "+2",
    "WILD": "WILD",
    "WILD_DRAW_FOUR": "+4",
}

# Four quadrant colours used inside the wild oval
_WILD_QUADS = [CARD_RED, CARD_BLUE, CARD_YELLOW, CARD_GREEN]


class CardComponent:
    def __init__(self, card, position=(0, 0), size=None):
        self.card = card        # dict: {color, type, value}
        self.pos = list(position)
        self.w = size[0] if size else CARD_W
        self.h = size[1] if size else CARD_H
        self.selected = False
        self.clickable = True
        self.index = 0         # position in hand — set by HandView

    # ------------------------------------------------------------------
    def render(self, surface):
        x, y = self.pos
        if self.selected:
            y -= 18             # lift selected card upward

        # Drop shadow
        _draw_shadow(surface, x + 5, y + 7, self.w, self.h, CARD_R)

        # Card body
        body = pygame.Rect(x, y, self.w, self.h)
        color = CARD_COLORS.get(self.card["color"], CARD_COLORS["WILD"])
        pygame.draw.rect(surface, color, body, border_radius=CARD_R)

        # Inner white border (inset 5 px)
        inset = pygame.Rect(x + 5, y + 5, self.w - 10, self.h - 10)
        pygame.draw.rect(surface, WHITE, inset, 2, border_radius=CARD_R - 3)

        # Centre oval + value
        oval_rect = pygame.Rect(x + 11, y + 16, self.w - 22, self.h - 32)
        if self.card["color"] == "WILD":
            _draw_wild_oval(surface, oval_rect)
        else:
            pygame.draw.ellipse(surface, WHITE, oval_rect)
            label = self._label()
            txt = _t.F_CARD_BIG.render(label, True, color)
            surface.blit(txt, txt.get_rect(center=oval_rect.center))

        # Corner labels
        lbl = self._label()
        _corner_label(surface, lbl, x + 6, y + 5, WHITE)
        _corner_label(surface, lbl, x + self.w - 6, y + self.h - 5, WHITE, anchor="bottomright")

        # Selected glow
        if self.selected:
            glow = pygame.Rect(x - 3, y - 3, self.w + 6, self.h + 6)
            pygame.draw.rect(surface, GLOW_SELECT, glow, 3, border_radius=CARD_R + 3)

    # ------------------------------------------------------------------
    def handle_event(self, event):
        if not self.clickable:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self._rect().collidepoint(event.pos)
        return False

    def set_selected(self, v):
        self.selected = v

    def set_clickable(self, v):
        self.clickable = v

    # ------------------------------------------------------------------
    def _label(self):
        if self.card["type"] == "NUMBER":
            return str(self.card["value"])
        return _LABELS.get(self.card["type"], "?")

    def _rect(self):
        x, y = self.pos
        if self.selected:
            y -= 18
        return pygame.Rect(x, y, self.w, self.h)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _draw_shadow(surface, x, y, w, h, r):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (*SHADOW, 120), (0, 0, w, h), border_radius=r)
    surface.blit(s, (x, y))


def _draw_wild_oval(surface, rect):
    """Four-quadrant coloured oval for wild cards."""
    x, y, w, h = rect.x, rect.y, rect.width, rect.height
    hw, hh = w // 2, h // 2

    quad_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(quad_surf, _WILD_QUADS[0], (0,  0,  hw, hh))
    pygame.draw.rect(quad_surf, _WILD_QUADS[1], (hw, 0,  hw, hh))
    pygame.draw.rect(quad_surf, _WILD_QUADS[2], (0,  hh, hw, hh))
    pygame.draw.rect(quad_surf, _WILD_QUADS[3], (hw, hh, hw, hh))

    # Mask to ellipse shape
    mask = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(mask, (255, 255, 255, 255), (0, 0, w, h))
    quad_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    surface.blit(quad_surf, (x, y))


def _corner_label(surface, text, x, y, color, anchor="topleft"):
    surf = _t.F_CARD_SMALL.render(text, True, color)
    r = surf.get_rect()
    setattr(r, anchor, (x, y))
    surface.blit(surf, r)


# ---------------------------------------------------------------------------
# Card back (for opponents)
# ---------------------------------------------------------------------------

def draw_card_back(surface, x, y, w=None, h=None):
    w = w or CARD_W
    h = h or CARD_H
    _draw_shadow(surface, x + 4, y + 5, w, h, CARD_R)
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, (30, 30, 42), rect, border_radius=CARD_R)
    inset = pygame.Rect(x + 5, y + 5, w - 10, h - 10)
    pygame.draw.rect(surface, (55, 60, 80), inset, 2, border_radius=CARD_R - 3)
    # Simple diagonal stripe pattern
    for i in range(-h, w, 12):
        pygame.draw.line(surface, (45, 50, 68),
                         (x + max(i, 0), y + max(-i, 0)),
                         (x + min(i + h, w), y + min(h, h + i)), 1)
