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
