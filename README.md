🃏 Custom UNO Online
📌 Overview

Custom UNO Online là một game UNO multiplayer (2–4 người) với:

Host room system (tạo phòng / join phòng)
Real-time synchronization
Luật UNO chuẩn + custom rules (0, 7, 8, stacking)
UI trực quan bằng Python (Pygame)

Mục tiêu chính của project:

Quản lý game state đúng
Xử lý logic rule phức tạp
Đồng bộ nhiều client
Thiết kế UI rõ ràng
🏗️ Project Structure
project/
  main.py
  run_server.py
  config.py

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
    ui_manager.py
⚙️ Requirements
pip install pygame

Python version:

Python 3.10+
▶️ How to Run
1. Start Server
python run_server.py

Output:

Starting Custom UNO Online server on 0.0.0.0:5000
2. Start Client

Mở terminal khác:

python main.py
🎮 Game Features
Core Gameplay
Number cards
Skip
Reverse
Draw Two (+2)
Wild
Wild Draw Four (+4)
Custom Rules
🔁 Rule of 0
Chọn chiều (clockwise / counter-clockwise)
Tất cả người chơi đổi bài
🔄 Rule of 7
Chọn 1 người chơi khác
Swap toàn bộ bài
⚡ Rule of 8 (Reaction)
Tất cả người chơi phải phản ứng nhanh
Người chậm nhất → rút 2 lá
📦 Stacking Rule
+2 → +2 hoặc +4
+4 → chỉ +4
Không stack → rút toàn bộ
🚫 No Win with Action Card

Không được thắng bằng:

Skip
Reverse
+2
Wild
+4
🧠 Architecture
Client (UI)
   ↓
Client Network
   ↓
Server (Host-authoritative)
   ↓
Game State (Logic)
Server là authority duy nhất
Client chỉ gửi request
Server validate + broadcast
👥 Team Responsibilities
1. Game Core
card.py
deck.py
game_state.py
rule_engine.py
2. Custom Rules
rule_zero.py
rule_seven.py
rule_eight.py
stacking_rule.py
3. Network
server.py
client.py
room_manager.py
protocol.py
4. UI
game_screen.py
lobby_screen.py
components/
🔄 Development Flow
1. Implement game core
2. Implement custom rules
3. Implement network
4. Implement UI
5. Integrate everything
🌿 Git Workflow
main → production
dev → integration
feature/* → development

Branches:

feature/game-core
feature/custom-rules
feature/network
feature/ui
