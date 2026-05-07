import pygame

from network.client import Client
from network.protocol import MessageType
from UI.theme import load_fonts
from UI.main_menu import MainMenu
from UI.room_screen import RoomScreen
from UI.lobby_screen import LobbyScreen
from UI.game_screen import GameScreen


class UIManager:
    def __init__(self):
        load_fonts()
        self.client = Client()
        self._screens = {}
        self._current_screen = None
        self._setup_screens()
        self._setup_callbacks()
        self.switch_screen("main_menu")

    def _setup_screens(self):
        self._screens["main_menu"]   = MainMenu()
        self._screens["room_screen"] = RoomScreen(self.client)
        self._screens["lobby"]       = LobbyScreen(self.client)
        self._screens["game"]        = GameScreen(self.client)

    def _setup_callbacks(self):
        self.client.on(MessageType.ROOM_CREATED,        self._on_room_created)
        self.client.on(MessageType.ROOM_JOINED,         self._on_room_joined)
        self.client.on(MessageType.PLAYER_LIST_UPDATED, self._on_player_list_updated)
        self.client.on(MessageType.GAME_STARTED,        self._on_game_started)
        self.client.on(MessageType.STATE_UPDATED,       self._on_state_updated)
        self.client.on(MessageType.REACTION_STARTED,    self._on_reaction_started)
        self.client.on(MessageType.REACTION_RESULT,     self._on_reaction_result)
        self.client.on(MessageType.GAME_ENDED,          self._on_game_ended)

    def switch_screen(self, screen_name):
        self._current_screen = self._screens.get(screen_name)

    def render(self, surface):
        if self._current_screen:
            self._current_screen.render(surface)

    def handle_event(self, event):
        if not self._current_screen:
            return

        action = self._current_screen.handle_event(event)
        if action is None:
            return

        # Main menu
        if action == "CREATE_ROOM":
            self._try_connect()
            self._screens["room_screen"].set_mode("CREATE")
            self.switch_screen("room_screen")
        elif action == "JOIN_ROOM":
            self._try_connect()
            self._screens["room_screen"].set_mode("JOIN")
            self.switch_screen("room_screen")
        elif action == "QUIT":
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Room screen
        elif action == "BACK":
            self.switch_screen("main_menu")
        elif action == "SUBMITTED":
            pass  # Wait for server ROOM_CREATED / ROOM_JOINED callback

        # Lobby
        elif action == "LEAVE_ROOM":
            self.switch_screen("main_menu")

        # Game result screen
        elif action == "menu":
            try:
                self.client.leave_room()
            except Exception:
                pass

            self._screens["game"].reset_for_new_game()
            self.switch_screen("main_menu")
        elif action == "quit":
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        pass

    # ------------------------------------------------------------------
    # Server callbacks (called from background receive thread)
    # ------------------------------------------------------------------

    def _on_room_created(self, message):
        data = message.get("data", {})
        lobby = self._screens["lobby"]
        lobby.set_room_data(data.get("room_code", ""), [], is_host=True)
        self.switch_screen("lobby")

    def _on_room_joined(self, message):
        data = message.get("data", {})
        lobby = self._screens["lobby"]
        lobby.set_room_data(data.get("room_code", ""), [], is_host=False)
        self.switch_screen("lobby")

    def _on_player_list_updated(self, message):
        data = message.get("data", {})
        lobby = self._screens["lobby"]
        host_id = data.get("host_id")
        is_host = host_id == self.client.player_id
        lobby.set_room_data(
            data.get("room_code", lobby.room_code),
            data.get("players", []),
            is_host=is_host,
        )

    def _on_game_started(self, message):
        game = self._screens["game"]
        game.my_id = self.client.player_id
        game.reset_for_new_game()
        self.switch_screen("game")

    def _on_state_updated(self, message):
        data = message.get("data", {})
        game = self._screens["game"]
        game.my_id = self.client.player_id
        game.set_game_state(data.get("state", {}))

    def _on_reaction_started(self, message):
        self._screens["game"].handle_reaction_started(message.get("data", {}))

    def _on_reaction_result(self, message):
        self._screens["game"].handle_reaction_result(message.get("data", {}))

    def _on_game_ended(self, message):
        data = message.get("data", {})
        game = self._screens["game"]
        game.set_game_state(data.get("state", game.game_state))
        self.switch_screen("game")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _try_connect(self):
        if not self.client.connected:
            try:
                self.client.connect()
            except Exception:
                pass
