# 🌐 Network - Custom UNO Online

## 📌 Overview

Module **Network** chịu trách nhiệm kết nối nhiều người chơi trong cùng một phòng và đồng bộ trạng thái game theo mô hình **host-authoritative**.

Client chỉ gửi yêu cầu hành động.  
Server/host là nơi kiểm tra, xử lý logic và broadcast trạng thái mới.

---

## 📂 Structure

```txt
network/
  client.py
  server.py
  protocol.py
  room_manager.py
  sync_manager.py
🧩 Responsibilities
[ ] Create room
[ ] Join room
[ ] Leave room
[ ] Start game
[ ] Send client actions to server
[ ] Validate message format
[ ] Connect room with GameState
[ ] Broadcast player list
[ ] Broadcast private game state to each player
[ ] Handle invalid actions
[ ] Handle disconnect before game starts
📡 protocol.py

Định nghĩa format message giữa client và server.

Message Format
{
  "type": "MESSAGE_TYPE",
  "data": {}
}
Main Message Types
CREATE_ROOM
JOIN_ROOM
LEAVE_ROOM
START_GAME

PLAY_CARD
DRAW_CARD
CHOOSE_COLOR
CHOOSE_ZERO_DIRECTION
CHOOSE_SEVEN_TARGET
SUBMIT_REACTION

ROOM_CREATED
ROOM_JOINED
PLAYER_LIST_UPDATED
GAME_STARTED
STATE_UPDATED
INVALID_ACTION
REACTION_STARTED
REACTION_RESULT
GAME_ENDED
ERROR
TODO
[ ] Define message type constants
[ ] Create standard message object
[ ] Encode message to JSON
[ ] Decode JSON to message
[ ] Validate required fields
[ ] Create error message
🏠 room_manager.py

Quản lý phòng chơi.

Room Responsibilities
[ ] Store room code
[ ] Store host id
[ ] Store players
[ ] Store player connections
[ ] Store GameState
[ ] Add player
[ ] Remove player
[ ] Check host permission
[ ] Check room can start
RoomManager Responsibilities
[ ] Generate unique room code
[ ] Create room
[ ] Join existing room
[ ] Leave room
[ ] Delete empty room
[ ] Find room by room code
[ ] Find room by player id
🔄 sync_manager.py

Đồng bộ dữ liệu từ server về client.

Responsibilities
[ ] Send message to one player
[ ] Broadcast message to all players in room
[ ] Broadcast player list
[ ] Broadcast game started
[ ] Broadcast game state
[ ] Broadcast invalid action
[ ] Broadcast reaction started
[ ] Broadcast reaction result
[ ] Broadcast game ended
Important Note

Khi broadcast game state, mỗi player phải nhận state riêng:

Player A sees:
- Own hand
- Other players' card count only

Player B sees:
- Own hand
- Other players' card count only

Không được gửi bài của tất cả người chơi cho mọi client.

🖥️ server.py

Server là authority chính của game.

Responsibilities
[ ] Start server
[ ] Accept client connections
[ ] Receive client messages
[ ] Decode message
[ ] Route message to correct handler
[ ] Validate action through GameState
[ ] Update game state
[ ] Broadcast result
[ ] Handle disconnect
Main Handlers
handle_create_room()
handle_join_room()
handle_leave_room()
handle_start_game()
handle_play_card()
handle_draw_card()
handle_choose_color()
handle_submit_reaction()
handle_disconnect()
💻 client.py

Client-side networking wrapper cho UI sử dụng.

UI không nên gọi socket trực tiếp.
UI chỉ nên gọi các method trong Client.

Responsibilities
[ ] Connect to server
[ ] Disconnect from server
[ ] Listen for server messages
[ ] Send message
[ ] Create room
[ ] Join room
[ ] Leave room
[ ] Start game
[ ] Play card
[ ] Draw card
[ ] Submit reaction
[ ] Register UI callbacks
Example UI Usage
client.create_room(player_name)
client.join_room(room_code, player_name)
client.start_game()
client.play_card(card_index)
client.draw_card()
client.submit_reaction()
🧠 Network Flow
Create Room
Client
  -> CREATE_ROOM
Server
  -> create Room
  -> create GameState
  -> add host player
  -> ROOM_CREATED
Join Room
Client
  -> JOIN_ROOM
Server
  -> validate room exists
  -> validate room not full
  -> add player
  -> PLAYER_LIST_UPDATED
Start Game
Host Client
  -> START_GAME
Server
  -> validate host
  -> validate 2-4 players
  -> GameState.start_game()
  -> GAME_STARTED
  -> STATE_UPDATED
Play Card
Client
  -> PLAY_CARD
Server
  -> validate current turn
  -> validate card legality
  -> GameState.play_card()
  -> STATE_UPDATED
Draw Card
Client
  -> DRAW_CARD
Server
  -> GameState.draw_card()
  -> STATE_UPDATED
🔐 Host-authoritative Rule

The server must validate:

[ ] Correct player's turn
[ ] Legal selected card
[ ] Valid card index
[ ] Valid color selection
[ ] Valid Rule 0 direction
[ ] Valid Rule 7 target
[ ] Valid Rule 8 reaction
[ ] Valid stacking action
[ ] No-win-with-action-card rule

Client-side validation is optional and only for better UI.
Server-side validation is required.

⚠️ Error Handling

Server should return INVALID_ACTION or ERROR when:

[ ] Room does not exist
[ ] Room is full
[ ] Game already started
[ ] Non-host tries to start game
[ ] Player acts outside their turn
[ ] Player sends illegal card index
[ ] Player plays illegal card
[ ] Player chooses invalid target
[ ] Player submits duplicate reaction
[ ] Player disconnects before game starts
🚀 Recommended Implementation Order
1. protocol.py
2. room_manager.py
3. sync_manager.py
4. server.py
5. client.py
📌 Development Status
🔲 protocol.py
🔲 room_manager.py
🔲 sync_manager.py
🔲 server.py
🔲 client.py
🔲 integration with game core
🔲 integration with UI
⚙️ Run Server

From project root:

python run_server.py

Expected output:

Starting Custom UNO Online server on 0.0.0.0:5000
⚙️ Run Client

From project root:

python main.py
Notes
Network không xử lý luật game trực tiếp.
Network chỉ nhận request, gọi Game Core, rồi broadcast kết quả.
Không gửi hand của người chơi này cho người chơi khác.
Server phải là nguồn dữ liệu cuối cùng.
