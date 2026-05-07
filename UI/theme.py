"""
Visual theme — CMYK-inspired palette, dark slate background.
All colours and layout constants live here so components stay consistent.
"""

import pygame

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

# Background / table
BG          = (28,  35,  45)   # dark slate — easy on the eyes
TABLE       = (35,  45,  58)   # felt area (play zone)
PANEL_BG    = (20,  28,  38)   # sidebar / HUD panels
PANEL_EDGE  = (50,  65,  80)   # subtle panel border

# CMYK-inspired card colours (muted, not neon)
CARD_RED    = (213, 43,  77)   # magenta-red
CARD_GREEN  = (0,   158, 96)   # clean process green
CARD_BLUE   = (0,   132, 199)  # cyan-blue
CARD_YELLOW = (225, 183, 0)    # golden yellow
CARD_WILD   = (25,  25,  35)   # near-black for wild

CARD_COLORS = {
    "RED":    CARD_RED,
    "GREEN":  CARD_GREEN,
    "BLUE":   CARD_BLUE,
    "YELLOW": CARD_YELLOW,
    "WILD":   CARD_WILD,
}

# Text
TEXT_LIGHT  = (235, 235, 240)
TEXT_MUTED  = (135, 148, 165)
TEXT_DARK   = (20,  20,  25)

# UI accents
WHITE       = (248, 248, 250)
SHADOW      = (12,  17,  25)
GLOW_SELECT = (255, 215, 50)   # selected-card highlight
WARNING     = (230, 100, 30)   # penalty warning
REACTION_BG = (180, 30,  60)   # reaction button red
REACTION_DONE = (60, 160, 80)  # reaction submitted green
BTN_BG      = (45,  58,  75)
BTN_HOVER   = (60,  78, 100)
BTN_BORDER  = (80, 100, 125)

# Direction indicators
DIR_CW      = (100, 210, 140)
DIR_CCW     = (100, 170, 230)

# ---------------------------------------------------------------------------
# Layout  (1280 × 720 window)
# ---------------------------------------------------------------------------

W, H = 1280, 720

CARD_W, CARD_H = 76, 110
CARD_R = 9          # border-radius

# Play area centre
PLAY_CX, PLAY_CY = 640, 310

# Player hand strip
HAND_Y = 540        # top-y of hand row
HAND_AVAILABLE_W = 1060  # max horizontal space for cards

# Status bar
STATUS_H = 52

# Opponent strip (top)
OPP_STRIP_Y = STATUS_H + 4
OPP_STRIP_H = 90

# ---------------------------------------------------------------------------
# Fonts  (call load_fonts() once after pygame.init())
# ---------------------------------------------------------------------------

F_CARD_BIG   = None   # card centre value
F_CARD_SMALL = None   # card corner labels
F_UI         = None   # general HUD
F_UI_LG      = None   # large HUD / popup title
F_UI_SM      = None   # small labels


def load_fonts():
    global F_CARD_BIG, F_CARD_SMALL, F_UI, F_UI_LG, F_UI_SM
    F_CARD_BIG   = pygame.font.SysFont("Arial", 28, bold=True)
    F_CARD_SMALL = pygame.font.SysFont("Arial", 13, bold=True)
    F_UI         = pygame.font.SysFont("Arial", 17)
    F_UI_LG      = pygame.font.SysFont("Arial", 30, bold=True)
    F_UI_SM      = pygame.font.SysFont("Arial", 13)
