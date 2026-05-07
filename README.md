🎨 UI - Custom UNO Online
📌 Overview

Module UI (User Interface) chịu trách nhiệm hiển thị toàn bộ giao diện game và xử lý tương tác người dùng.

UI được xây dựng theo nguyên tắc:

Tách biệt hoàn toàn với Game Core
Không xử lý logic game
Chỉ hiển thị state từ server
Gửi action qua client/network

Trong game UNO, UI đóng vai trò rất quan trọng vì trải nghiệm người chơi phụ thuộc nhiều vào visual clarity và UX flow .

📂 Structure
UI/
  components/
    card_component.py
    hand_view.py
    opponent_panel.py
    status_panel.py
    popup_select_color.py
    popup_select_target.py
    reaction_button.py
    result_screen.py

  main_menu.py
  room_screen.py
  lobby_screen.py
  game_screen.py
  ui_manager.py
🧩 Responsibilities
[ ] Hiển thị game state
[ ] Hiển thị bài người chơi
[ ] Hiển thị số bài đối thủ
[ ] Hiển thị lượt chơi
[ ] Hiển thị hiệu ứng (penalty, direction)
[ ] Nhận input từ user (click, select)
[ ] Gửi action đến client
[ ] Hiển thị popup (color, target, reaction)
[ ] Hiển thị kết quả game
🖥️ Screens
1. Main Menu
[ ] Nút Create Room
[ ] Nút Join Room
[ ] Nút Quit
2. Room Screen
[ ] Input player name
[ ] Input room code (join mode)
[ ] Button confirm
[ ] Button back
3. Lobby Screen
[ ] Hiển thị room code
[ ] Danh sách player
[ ] Nút Start Game (host only)
[ ] Nút Leave Room
4. Game Screen (Quan trọng nhất)

Game screen gồm nhiều thành phần:

[ ] HandView (bài của player)
[ ] OpponentPanel (đối thủ)
[ ] StatusPanel (trạng thái game)
[ ] Draw button
[ ] Play card interaction
[ ] Popup system
[ ] Reaction button

📌 Một UI tốt cần:

Rõ ràng (ai đang chơi, đang có gì xảy ra)
Phản hồi nhanh
Không gây nhầm lẫn cho player
🧱 Components
🃏 card_component.py
[ ] Render 1 lá bài
[ ] Hiển thị màu + value
[ ] Detect click
[ ] Highlight selected card
✋ hand_view.py
[ ] Hiển thị toàn bộ bài player
[ ] Sắp xếp vị trí card
[ ] Cho phép chọn card
👥 opponent_panel.py
[ ] Hiển thị danh sách đối thủ
[ ] Hiển thị số lượng bài
📊 status_panel.py
[ ] Hiển thị current player
[ ] Hiển thị current color
[ ] Hiển thị direction
[ ] Hiển thị pending penalty
[ ] Hiển thị top discard
🎨 popup_select_color.py
[ ] Popup chọn màu (Wild)
[ ] 4 button màu
🎯 popup_select_target.py
[ ] Popup chọn target (Rule 7)
[ ] Danh sách player
⚡ reaction_button.py
[ ] Button cho Rule 8
[ ] Chỉ click được 1 lần
[ ] Có thể hiển thị countdown
🏁 result_screen.py
[ ] Hiển thị winner
[ ] Button back to menu
🧠 UI Flow
MainMenu
  ↓
RoomScreen
  ↓
LobbyScreen
  ↓
GameScreen
  ↓
ResultScreen
🔗 Integration với Network

UI không gọi Game Core trực tiếp.

Flow đúng:

UI → Client → Server → GameState → Server → UI

Ví dụ:

# UI
client.play_card(card_index)

# Server xử lý → gửi state mới

# UI nhận:
on_state_updated(state)
⚠️ Important Rules
[ ] Không viết logic game trong UI
[ ] Không validate game rule ở UI
[ ] Không lưu state game riêng
[ ] Luôn lấy state từ server
🎮 Event Handling

UI cần xử lý:

[ ] Mouse click
[ ] Card selection
[ ] Button click
[ ] Popup interaction
🚀 Recommended Implementation Order
1. card_component.py
2. hand_view.py
3. status_panel.py
4. opponent_panel.py
5. main_menu.py
6. room_screen.py
7. lobby_screen.py
8. game_screen.py
9. ui_manager.py
📌 Development Status
🔲 components
🔲 main_menu
🔲 room_screen
🔲 lobby_screen
🔲 game_screen
🔲 ui_manager
🔲 integration with client
💡 Notes
UI phải đơn giản nhưng rõ ràng
Không cần đồ họa fancy, chỉ cần:
dễ nhìn
dễ hiểu
không bug

UNO là game nhanh → UI phải phản hồi nhanh.
🎯 Custom Rules - Custom UNO Online
📌 Overview

Module Custom Rules triển khai các luật mở rộng của UNO, bao gồm:

Rule of 0
Rule of 7
Rule of 8 (Reaction Event)
Stacking Rule (+2 / +4)

Các luật này là house rules phổ biến, không nằm hoàn toàn trong luật chuẩn UNO nhưng được dùng rộng rãi trong các phiên bản mở rộng .

📂 Structure
game/custom_rules/
  rule_zero.py
  rule_seven.py
  rule_eight.py
  stacking_rule.py
🔁 Rule of 0
📖 Description

Khi người chơi đánh lá 0:

Chọn hướng: clockwise hoặc counter-clockwise
Tất cả người chơi chuyển toàn bộ bài
Việc chuyển diễn ra đồng thời

📌 Đây là rule phổ biến trong biến thể 7-0 rule

🧠 Logic cần xử lý
[ ] Validate direction
[ ] Lưu toàn bộ hand hiện tại
[ ] Xoay danh sách hand theo direction
[ ] Gán lại hand cho từng player
🔄 Rule of 7
📖 Description

Khi đánh lá 7:

Người chơi chọn 1 target
Hai người swap toàn bộ bài

📌 Đây là rule phổ biến trong UNO house rules

🧠 Logic cần xử lý
[ ] Validate target_player_id
[ ] Không cho chọn chính mình
[ ] Swap hand giữa 2 player
⚡ Rule of 8 (Reaction Event)
📖 Description

Khi đánh lá 8:

Trigger một sự kiện phản ứng nhanh
Tất cả người chơi phải click "reaction"
Người phản ứng chậm nhất bị phạt
🧠 Behavior
[ ] Host start event
[ ] Set time window (e.g. 3s)
[ ] Mỗi player chỉ được submit 1 lần
[ ] Track timestamp của mỗi response
[ ] Nếu không response → bị tính là chậm nhất
[ ] Player chậm nhất → draw 2 cards
📦 Stacking Rule (+2 / +4)
📖 Description

Cho phép stack penalty:

Sau +2 → có thể đánh +2 hoặc +4
Sau +4 → chỉ được đánh +4
Penalty sẽ cộng dồn

📌 Đây là rule phổ biến nhưng không phải luật chuẩn UNO

🧠 Logic
[ ] Xác định card có phải penalty không
[ ] So sánh penalty value (>= previous)
[ ] Cộng dồn penalty
[ ] Nếu không stack:
    → player phải draw toàn bộ
    → mất lượt
🚫 No Win with Action Card
📖 Description

Không được thắng nếu lá cuối là:

Skip
Reverse
Draw Two
Wild
Wild Draw Four
🧠 Logic
[ ] Nếu player còn 1 lá
[ ] Và lá đó là action card
→ không cho phép đánh
🔗 Integration với Game Core

Các rule sẽ được gọi từ:

game/game_state.py

Ví dụ:

# TODO example usage
RuleZero.apply(players, direction)
RuleSeven.apply(players, player_id, target_id)
RuleEight.start_event(players)
StackingRule.can_stack(card, last_penalty)
⚠️ Notes
Tất cả rule phải được validate ở server (host)
Client chỉ gửi request → server quyết định kết quả
Rule 8 cần đồng bộ realtime (quan trọng nhất)
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
