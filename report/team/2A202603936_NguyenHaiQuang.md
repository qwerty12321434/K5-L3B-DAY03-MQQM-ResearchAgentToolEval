# Báo cáo cá nhân — Nguyễn Hải Quang (2A202603936)

## 1. Thông tin thành viên

- Họ tên: Nguyễn Hải Quang
- MSSV: 2A202603936
- Email: quangnh2004@gmail.com

## 2. Phần việc phụ trách

- Phụ trách eval nhóm, UI và live chat, tổng hợp báo cáo nhóm; phối hợp với Minh hoàn thành bài lab.

## 3. Đóng góp cụ thể

- Thiết kế bộ `eval_group.json` gồm đúng 10 case: 5 single turn và 5 multi turn. Một case kiểm tra việc gọi tool mới `dedupe_sources`.
- Run group trên Ollama `llama3.2:3b` đo đủ 10/10 case, không có provider error; 5 case pass. Các lỗi còn lại gồm thiếu `max_results`, gọi tool cho yêu cầu chỉ lập kế hoạch, không hỏi khi thiếu handle và xử lý chưa đúng việc sửa/hủy bản nháp gửi.
- Triển khai UI Streamlit dùng vòng lặp tool của `chat.py`; giao diện chặn tool `send` và chỉ cho xem trước nội dung Telegram. Transcript nhóm có bốn lượt: tìm tin, hỏi URL còn thiếu, đọc URL sau khi bổ sung và xin xác nhận bản nháp.
- Tổng hợp báo cáo nhóm với bảng version, phân tích lỗi, eval nhóm, transcript và giới hạn của phép đo. Link Cloudflare Tunnel chỉ hoạt động khi máy demo và tunnel còn chạy; cần kiểm tra lại trước khi trình diễn.

Minh xác nhận hai thành viên cùng thực hiện bài nhóm và Quang phụ trách các phần trên. Các file được lưu trong commit bài nhóm `b0094a1`.

## 4. Bằng chứng

- [Bộ eval nhóm](../../starter_v0/data/eval_group.json) và [run group](../../starter_v0/runs/v3_B_group_ollama_20261110T191412574874.json).
- [UI Streamlit](../../starter_v0/app.py), [vòng lặp chat](../../starter_v0/chat.py), [transcript live](../../starter_v0/transcripts/v3_ollama_20261110T191413259029.transcript.json).
- [Báo cáo nhóm](group_report.md), commit nhóm `b0094a1`.
- Lịch sử Git chưa tách commit kỹ thuật theo từng thành viên; phần việc của Quang được ghi trong `TEAM.md`.
- Codex hỗ trợ biên tập báo cáo trong lượt này. Kết quả eval được kiểm tra bằng run JSON; hành vi UI/chat được đối chiếu với transcript.

## 5. Tự đánh giá

- Bộ eval nhóm đủ 10 case, run hợp lệ và transcript thể hiện agent hỏi lại khi thiếu URL. Hạn chế rõ nhất là chỉ 5/10 case nhóm pass, còn lỗi khi thiếu handle và khi người dùng sửa hoặc hủy yêu cầu gửi. Hướng cải thiện là thêm case hồi quy cho hai tình huống đó rồi đo lại trên cùng model.
