"""
Rules Screen — displays all game rules and special card descriptions.
"""

import pygame
import UI.theme as _t
from UI.theme import (
    BG, PANEL_BG, PANEL_EDGE,
    TEXT_LIGHT, TEXT_MUTED, WARNING, GLOW_SELECT,
    BTN_BG, BTN_HOVER, BTN_BORDER,
    CARD_RED, CARD_GREEN, CARD_BLUE, CARD_YELLOW,
    W, H)

_COL_L = 55
_COL_R = 660
_COL_W = 560
_Y_START = 115
_LINE_H = 22
_SEC_GAP = 16

_LEFT_SECTIONS = [
    ("STANDARD PLAY", TEXT_LIGHT, [
        "Each turn: play one legal card or draw from the pile.",
        "Legal card: same color, same number/type, or Wild.",
        "Draw: if the drawn card is legal you may play it.",
        "Otherwise the turn ends after drawing.",
    ]),
    ("STANDARD CARD TYPES", TEXT_LIGHT, [
        "Skip    — next player loses their turn.",
        "Reverse — reverses play direction (R / L).",
        "+2      — next player draws 2  (stackable).",
        "Wild    — play anytime, then choose a color.",
        "+4      — play anytime, next draws 4  (stackable).",
    ]),
    ("WIN CONDITION", GLOW_SELECT, [
        "First player to empty their hand wins.",
        "CANNOT win by playing an action or Wild card.",
        "Forbidden last cards: Skip, Reverse, +2, Wild, +4.",
        "If only a forbidden card remains, draw instead.",
    ]),
]

_RIGHT_SECTIONS = [
    ("HOUSE RULE: Card 0  (Pass Hands)", CARD_GREEN, [
        "Choose direction R (clockwise) or L (counter-clockwise).",
        "ALL players simultaneously pass their entire hand.",
        "Hand passing only — does NOT change turn order.",
    ]),
    ("HOUSE RULE: Card 7  (Swap Hands)", CARD_BLUE, [
        "Choose one opponent from the target menu.",
        "You and that opponent instantly swap entire hands.",
        "The swap is synchronized across all clients.",
    ]),
    ("HOUSE RULE: Card 8  (Reaction Event)", CARD_RED, [
        "A reaction event is triggered for ALL players.",
        "Everyone must click the REACT! button in time.",
        "The LAST player to click draws 2 cards as penalty.",
        "Players who miss the 3-second window also draw 2.",
        "Multiple slow/missing players all receive the penalty.",
    ]),
    ("STACKING  (+2 / +4)", WARNING, [
        "If facing a draw penalty you may stack a card >= it.",
        "After +2: you may respond with +2 or +4.",
        "After +4: you may only respond with another +4.",
        "The first player who cannot (or chooses not to) stack",
        "draws ALL accumulated cards and loses the turn.",
        "Example: +2 -> +2 -> +4 -> no stack = draw 8 cards.",
    ]),
]


class RulesScreen:
    def __init__(self):
        btn_w, btn_h = 240, 48
        self._back_btn = pygame.Rect(W // 2 - btn_w // 2, H - 68, btn_w, btn_h)

    def render(self, surface):
        surface.fill(BG)

        title = _t.F_UI_LG.render("Custom UNO  —  Game Rules", True, TEXT_LIGHT)
        surface.blit(title, title.get_rect(centerx=W // 2, top=28))

        sep_y = 72
        pygame.draw.line(surface, PANEL_EDGE, (40, sep_y), (W - 40, sep_y), 1)

        _render_sections(surface, _LEFT_SECTIONS, _COL_L, _Y_START, _COL_W)
        _render_sections(surface, _RIGHT_SECTIONS, _COL_R, _Y_START, _COL_W)

        pygame.draw.line(surface, PANEL_EDGE, (W // 2 - 4, 80), (W // 2 - 4, H - 80), 1)

        sep_y2 = H - 80
        pygame.draw.line(surface, PANEL_EDGE, (40, sep_y2), (W - 40, sep_y2), 1)

        mouse = pygame.mouse.get_pos()
        bg = BTN_HOVER if self._back_btn.collidepoint(mouse) else BTN_BG
        pygame.draw.rect(surface, bg, self._back_btn, border_radius=8)
        pygame.draw.rect(surface, BTN_BORDER, self._back_btn, 1, border_radius=8)
        lbl = _t.F_UI.render("Back to Menu", True, TEXT_LIGHT)
        surface.blit(lbl, lbl.get_rect(center=self._back_btn.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._back_btn.collidepoint(event.pos):
                return "BACK"
        return None


def _render_sections(surface, sections, x, y_start, col_w):
    y = y_start
    for header, hdr_color, lines in sections:
        hdr = _t.F_UI.render(header, True, hdr_color)
        surface.blit(hdr, (x, y))
        y += _LINE_H + 4

        for line in lines:
            txt = _t.F_UI_SM.render("  " + line, True, TEXT_MUTED)
            surface.blit(txt, (x + 8, y))
            y += _LINE_H

        y += _SEC_GAP
