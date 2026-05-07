"""
Hand View — player's own cards displayed at the bottom of the screen.
"""

import pygame
from UI.theme import CARD_W, CARD_H, HAND_Y, HAND_AVAILABLE_W, W
from UI.components.card_component import CardComponent


class HandView:
    def __init__(self):
        self.components = []
        self.selected_index = None

    def set_cards(self, cards):
        """cards: list of card dicts from to_private_dict."""
        self.components = []
        self.selected_index = None
        n = len(cards)
        if n == 0:
            return

        # Compute step so all cards fit within HAND_AVAILABLE_W
        max_step = CARD_W + 8
        if n > 1:
            step = min(max_step, (HAND_AVAILABLE_W - CARD_W) // (n - 1))
        else:
            step = max_step

        total_w = CARD_W + step * (n - 1)
        start_x = W // 2 - total_w // 2

        for i, card in enumerate(cards):
            cc = CardComponent(card, (start_x + i * step, HAND_Y))
            cc.index = i
            self.components.append(cc)

    def render(self, surface):
        # Render unselected first so selected renders on top
        for cc in self.components:
            if not cc.selected:
                cc.render(surface)
        for cc in self.components:
            if cc.selected:
                cc.render(surface)

    def handle_event(self, event):
        """Returns clicked card index, or None."""
        for cc in self.components:
            if cc.handle_event(event):
                clicked = cc.index
                # Toggle selection
                if self.selected_index == clicked:
                    self.clear_selection()
                    return None
                self.clear_selection()
                cc.set_selected(True)
                self.selected_index = clicked
                return clicked
        return None

    def clear_selection(self):
        self.selected_index = None
        for cc in self.components:
            cc.set_selected(False)

    def set_playable(self, playable_indices):
        """Dim cards that cannot be played."""
        for cc in self.components:
            cc.set_clickable(cc.index in playable_indices)
