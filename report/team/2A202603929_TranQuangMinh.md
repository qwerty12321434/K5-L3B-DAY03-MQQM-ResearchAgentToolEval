# Báo cáo cá nhân — Trần Quang Minh (2A202603929)

## 1. Thông tin thành viên

- Họ tên: Trần Quang Minh
- MSSV: 2A202603929
- Email: tqminhhn04@gmail.com

## 2. Phần việc phụ trách

- CP1–CP3: setup, baseline v0, các vòng tối ưu v1–v3, tool mới và unit test.
- Phối hợp với Quang hoàn thành bài nhóm; chịu trách nhiệm chính bốn phần đầu.

## 3. Đóng góp cụ thể

- Chuẩn bị baseline v0 và các vòng cải thiện prompt/tool v1–v3; ghi giả thuyết, hash và metric trong version log. Run v0 và v1 trên OpenRouter đều đo đủ 20/20 case, không có provider error; case accuracy tăng từ 45% lên 70%.
- Đối chiếu chuỗi so sánh cùng model Ollama: v1-local đạt 15%, v2 đạt 30%, v3 đạt 50%, mỗi run đo đủ 20/20 case và không có provider error. Không dùng chênh lệch giữa v1 OpenRouter và v2 Ollama để kết luận về tác dụng riêng của thay đổi prompt/tool.
- Phụ trách phần tool mới `dedupe_sources`: implementation, `TOOL.md`, đăng ký trong registry và `tools.yaml`, cùng ba test trong `test_tools_todo.py`. Case eval nhóm `G-S01-dedupe-sources` kiểm tra model route tới tool này.
- Run `v3-integrated` đạt 40%, thấp hơn v3 50%. Lượt tích hợp thay đổi đồng thời tool declaration và giới hạn đầu ra Ollama, nên chưa thể quy mức giảm cho một nguyên nhân duy nhất.
- Sau khi điền `.env` trên máy này, chạy lại toàn bộ unit test: 73 passed, 14 skipped, 0 failed. Lượt preflight OpenRouter với model ghi trong báo cáo trả HTTP 401 (`Missing Authentication header`), nên key mới chưa được xác nhận hoạt động và chưa chạy thêm eval.

## 4. Bằng chứng

- [Version log](../../starter_v0/artifacts/version_log.csv), [báo cáo nhóm](group_report.md), [tool mới](../../starter_v0/tools/dedupe_sources/tool.py), [unit test](../../starter_v0/tests/test_tools_todo.py), [output pytest](../../starter_v0/analysis/pytest_20261110.txt).
- Run: [v0 OpenRouter](../../starter_v0/runs/v0_B_base_openrouter_20261110T185140539504.json), [v1 OpenRouter](../../starter_v0/runs/v1_B_base_openrouter_20261110T185436626437.json), [v1-local](../../starter_v0/runs/v1-local_B_base_ollama_20261110T190305548398.json), [v2](../../starter_v0/runs/v2_B_base_ollama_20261110T190444602025.json), [v3](../../starter_v0/runs/v3_B_base_ollama_20261110T190656563598.json), [v3-integrated](../../starter_v0/runs/v3-integrated_B_base_ollama_20261110T191634426601.json).
- Commit bài nhóm: `b0094a1`. Lịch sử Git chưa tách commit kỹ thuật theo từng thành viên; phần việc cá nhân được ghi trong `TEAM.md`.
- Codex hỗ trợ biên tập báo cáo trong lượt này. Kết quả kỹ thuật được đối chiếu với run JSON và lệnh `pytest`; kết quả preflight thất bại được ghi riêng ở mục 3.

## 5. Tự đánh giá

- Các run được dẫn đều đo đủ case; chuỗi v0/v1 cùng OpenRouter và v1-local/v2/v3 cùng Ollama cho phép so sánh trong từng model. Hạn chế là cấu hình tích hợp đạt 40%, thấp hơn v3 50%, và việc đổi đồng thời YAML cùng giới hạn đầu ra không cho biết nguyên nhân riêng. Cần thử một thay đổi mỗi lượt trên cùng model để xác định nguyên nhân. Key OpenRouter mới cần được kiểm tra lại vì preflight hiện trả 401.
