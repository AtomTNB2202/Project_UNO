# 🧠 Game Core - Custom UNO Online

## 📌 Overview

Module **Game Core** chịu trách nhiệm xử lý toàn bộ logic chính của game UNO.

Phần này không phụ thuộc vào UI hoặc network.  
UI và server chỉ gọi các hàm từ Game Core để cập nhật trạng thái game.

---

## 📂 Structure

```txt
game/
  card.py
  deck.py
  player.py
  game_state.py
  rule_engine.py
  turn_manager.py
🃏 card.py

Quản lý thông tin của một lá bài.

Responsibilities
[ ] Định nghĩa màu bài
[ ] Định nghĩa loại bài
[ ] Lưu thông tin card: color, type, value
[ ] Kiểm tra card có phải number card không
[ ] Kiểm tra card có phải action card không
[ ] Kiểm tra card có phải wild card không
[ ] Trả về penalty value của card
👤 player.py

Quản lý thông tin người chơi và bài trên tay.

Responsibilities
[ ] Lưu player_id
[ ] Lưu player name
[ ] Lưu hand của người chơi
[ ] Thêm 1 lá bài vào hand
[ ] Thêm nhiều lá bài vào hand
[ ] Xóa lá bài theo index
[ ] Đếm số lá bài
[ ] Kiểm tra người chơi đã hết bài chưa
[ ] Convert player data sang dictionary
📚 deck.py

Quản lý draw pile và discard pile.

Responsibilities
[ ] Tạo bộ bài UNO cơ bản
[ ] Shuffle draw pile
[ ] Rút 1 lá bài
[ ] Rút nhiều lá bài
[ ] Đưa bài vào discard pile
[ ] Lấy top card của discard pile
[ ] Rebuild draw pile khi hết bài
🔄 turn_manager.py

Quản lý lượt chơi và chiều chơi.

Responsibilities
[ ] Lưu current player index
[ ] Lưu direction hiện tại
[ ] Chuyển sang lượt tiếp theo
[ ] Skip người chơi tiếp theo
[ ] Reverse chiều chơi
[ ] Trả về direction dạng text
✅ rule_engine.py

Kiểm tra tính hợp lệ của hành động đánh bài.

Responsibilities
[ ] Check same color
[ ] Check same number
[ ] Check same action type
[ ] Check Wild / Wild Draw Four
[ ] Check stacking +2 / +4
[ ] Check no-win-with-action-card rule
🎮 game_state.py

File trung tâm quản lý trạng thái toàn bộ game.

Responsibilities
[ ] Lưu danh sách players
[ ] Lưu deck
[ ] Lưu turn manager
[ ] Lưu current color
[ ] Lưu pending penalty
[ ] Lưu winner
[ ] Add player
[ ] Remove player
[ ] Start game
[ ] Play card
[ ] Draw card
[ ] Apply card effect
[ ] Check winner
[ ] Export game state cho UI/network
🔗 Relationship with Other Modules
UI
 ↓
network/client.py
 ↓
network/server.py
 ↓
game/game_state.py
 ↓
game core files

Game Core là lớp xử lý logic chính.
Server gọi Game Core để validate và cập nhật state.
UI chỉ hiển thị state đã được xử lý.

🧪 Suggested Manual Tests
[ ] Tạo GameState
[ ] Add 2 players
[ ] Start game
[ ] Check mỗi player có 7 lá
[ ] Check discard pile có top card
[ ] Check current player
[ ] Test play legal card
[ ] Test illegal card
[ ] Test draw card
[ ] Test skip
[ ] Test reverse
[ ] Test +2
[ ] Test +4
[ ] Test no-win-with-action-card
🚀 Recommended Implementation Order
1. card.py
2. player.py
3. deck.py
4. turn_manager.py
5. rule_engine.py
6. game_state.py
