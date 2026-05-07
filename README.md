# Custom UNO Online

## Overview

Custom UNO Online is a Python/Pygame multiplayer UNO game for 2 to 4 players.
It includes a host-authoritative socket server, synchronized game state, standard
UNO gameplay, custom rules, and a playable UI.

## Features

- Create and join rooms with a room code
- Host-controlled match start
- 2 to 4 player multiplayer over sockets
- Server-authoritative shuffling, dealing, validation, turn order, effects, and win checking
- Standard UNO cards: number, Skip, Reverse, Draw Two, Wild, Wild Draw Four
- Custom Rule 0: choose direction and pass hands
- Custom Rule 7: choose a target and swap hands
- Custom Rule 8: reaction event, slowest responder draws 2 cards
- Stacking penalties for +2 and +4
- Result screen and disconnect handling

## Project Structure

```text
Project_UNO/
  main.py
  run_server.py
  config.py
  requirements.txt

  game/
    card.py
    deck.py
    player.py
    game_state.py
    rule_engine.py
    turn_manager.py
    custom_rules/

  network/
    client.py
    server.py
    protocol.py
    room_manager.py
    sync_manager.py

  UI/
    components/
    main_menu.py
    room_screen.py
    lobby_screen.py
    game_screen.py
    rules_screen.py
    ui_manager.py
```

## Requirements

- Python 3.10+
- pygame

Install dependencies:

```bash
pip install -r requirements.txt
```

## How To Run

Start the server:

```bash
python run_server.py
```

Start each client in a separate terminal:

```bash
python main.py
```

One player creates a room and shares the room code. Other players join using that
code. The host can start once at least 2 players are in the room.

## Gameplay Notes

The server is the final authority. Clients only send requests such as play card,
draw card, choose color, choose target, or submit reaction. The server validates
each request and broadcasts the resulting state.

If a player leaves during a match, they are removed from the active game. The game
continues while at least 2 players remain. If only 1 player remains, that player
wins. If the host leaves and at least 2 players remain, a new host is assigned.
