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
