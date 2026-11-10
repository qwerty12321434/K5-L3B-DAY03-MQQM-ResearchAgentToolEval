# Team

## Thông tin nhóm

- Tên nhóm: MQQM
- Lớp: L3B
- Repo nhóm: [K5-L3B-DAY03-MQQM-ResearchAgentToolEval](https://github.com/qwerty12321434/K5-L3B-DAY03-MQQM-ResearchAgentToolEval)
- Nhánh nộp: `main`
- Commit bài nhóm hiện có: `b0094a1`; commit chốt sau khi hoàn tất báo cáo: cập nhật khi nộp.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Hải Quang | 2A202603936 |       |        | Phụ trách eval nhóm, UI/live chat và báo cáo nhóm. |
|   2 | Trần Quang Minh | 2A202603929 | tqminhhn04@gmail.com |        | Phụ trách setup, baseline v0, tối ưu v1–v3, tool mới và unit test. |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Minh xác nhận hai thành viên cùng thực hiện bài nhóm. Bảng trên ghi phần mỗi người phụ trách; commit `b0094a1` là bằng chứng bài nhóm đã đưa lên repo. Metadata của commit không dùng để thay thế thông tin đóng góp do thành viên xác nhận.

## TranQuangMinh-2A202603929

### Phần việc phụ trách

- Phụ trách bốn phần đầu: setup, baseline v0, tối ưu v1–v3, tool mới và unit test.

### Đóng góp cụ thể

- Chuẩn bị và đối chiếu baseline, các vòng tối ưu với `artifacts/version_log.csv`: v0/v1 cùng OpenRouter đạt 45%/70%; v1-local/v2/v3 cùng Ollama đạt 15%/30%/50%. Run tích hợp sau đó đạt 40%.
- Phần tool mới và test: `dedupe_sources` đã đăng ký, có `TOOL.md`, một case eval nhóm và ba unit test.

### Bằng chứng

- `starter_v0/artifacts/version_log.csv`, `starter_v0/runs/`, `starter_v0/tools/dedupe_sources/`, `starter_v0/tests/test_tools_todo.py`.
- Báo cáo cá nhân: `report/team/2A202603929_TranQuangMinh.md`.
- Commit bài nhóm: `b0094a1`. Lịch sử Git hiện chưa tách commit kỹ thuật theo từng thành viên.

## NguyenHaiQuang-2A202603936

### Phần việc phụ trách

- Phụ trách eval nhóm, UI/live chat và tổng hợp báo cáo nhóm.

### Đóng góp cụ thể

- Hoàn thành 10 case eval nhóm và run group; triển khai UI Streamlit, ghi transcript live và tổng hợp báo cáo nhóm.

### Bằng chứng

- `starter_v0/data/eval_group.json`, `starter_v0/runs/v3_B_group_ollama_20261110T191412574874.json`, `starter_v0/app.py`, `starter_v0/transcripts/`, `report/team/group_report.md`.
- Báo cáo cá nhân: `report/team/2A202603936_NguyenHaiQuang.md`.
- Commit bài nhóm: `b0094a1`. Lịch sử Git hiện chưa tách commit kỹ thuật theo từng thành viên.
