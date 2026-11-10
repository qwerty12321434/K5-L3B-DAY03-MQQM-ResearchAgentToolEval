# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: MQQM (L3B)
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider cho baseline: OpenRouter, model `nvidia/nemotron-3.5-lightning:free`. Sau khi OpenRouter hết quota trong lúc đo v2, dùng Ollama với `llama3.2:3b` và chạy lại v0, v1 để có mốc so sánh cùng model.

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research Agent tìm nguồn trên web và X, đọc URL, tra policy nội bộ và định dạng nguồn thành bản tin. Tool `dedupe_sources` gộp các nguồn trùng trong danh sách đã có.

**Cách chạy UI:**

Từ thư mục gốc của repo trên Windows:

```powershell
cd starter_v0
uv venv --allow-existing .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Điền key vào `starter_v0/.env` trước khi chạy UI. Đặt `OPENROUTER_MODEL` trùng với model dùng trong eval để UI dùng cùng cấu hình. [Hướng dẫn cấu hình](../../docs/TOOL-SETUP.md)

Khi OpenRouter hết quota, UI có thể chạy bằng Ollama. Bật Ollama, rồi đặt hai biến sau trong PowerShell trước khi chạy lệnh Streamlit ở trên.

```powershell
$env:RESEARCH_PROVIDER = 'ollama'
$env:OLLAMA_MODEL = 'llama3.2:3b'
```

**Link dùng thử.** Demo hiện dùng Ollama. Đã kiểm tra trang trả HTTP 200 và kết nối WebSocket của Streamlit hoạt động. Tunnel còn mở khi máy chủ demo đang chạy. Luồng Telegram trên UI chỉ xem trước nội dung. [Mở demo](https://cordless-excess-sys-friend.trycloudflare.com)

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi thêm dữ kiện hoặc xin xác nhận. | Không |
| `timeline` | Lấy bài đăng gần đây của một tài khoản X. | Không |
| `social_search` | Tìm bài đăng trên X theo từ khóa. | Không |
| `lookup` | Tra cứu thông tin hoặc tin tức trên web. | Không |
| `fetch` | Đọc nội dung của một URL. | Không |
| `format` | Trình bày nguồn có sẵn thành bản tin Markdown. | Không |
| `policy` | Tìm trong handbook nội bộ. | Không |
| `papers` | Tìm bài nghiên cứu trên arXiv. | Không |
| `paper_text` | Đọc văn bản PDF từ arXiv. | Không |
| `send` | Gửi bản tin đã xác nhận qua Telegram trong CLI nếu đã cấu hình. | Không |
| `dedupe_sources` | Gộp URL trùng và giữ mục xuất hiện đầu tiên. | Có |

### A3. Câu hỏi mẫu để thử

1. Tìm 3 tin về pin thể rắn trên web trong tuần này.
2. Tóm tắt bài này giúp mình. Khi agent hỏi lại, bổ sung `https://docs.python.org/3/tutorial/`.
3. Gộp link trùng trong danh sách `https://example.org/report#intro`, `https://example.org/report#results` và `https://example.org/summary`.
4. Chuẩn bị đăng lên Telegram câu “Buổi chia sẻ bắt đầu lúc 16h” và hỏi mình xác nhận trước.

## 3. Giải pháp

- `dedupe_sources` xử lý các URL HTTP(S) đã có. Tool giữ metadata và thứ tự của nguồn đầu tiên, bỏ qua chữ hoa/thường của tên miền và phần fragment, đồng thời giữ các URL có query khác nhau. [Contract của tool](../../starter_v0/tools/dedupe_sources/TOOL.md)
- Streamlit dùng lại vòng lặp tool của CLI và lưu lịch sử theo phiên. Bản demo Telegram chỉ xem trước. Vòng lặp chỉ thực thi tool đã cung cấp cho model, nên lời gọi `send` do model tự sinh trong UI cũng bị chặn. [Code UI](../../starter_v0/app.py) · [Vòng lặp chat](../../starter_v0/chat.py)
- Sau baseline, v1 thay quy tắc quyết định hành động để hỏi khi thiếu dữ kiện, giới hạn phạm vi research, xin xác nhận gửi và cho phép nhiều lời gọi độc lập.
- Ở v2, mô tả tool làm rõ khi nào dùng từng tool và cách tách chủ đề, loại tin, thời gian và số lượng thành các tham số riêng.
- Ở v3, prompt dùng quy tắc routing ngắn kèm ví dụ tiếng Việt để phân biệt nguồn web, X và URL cụ thể. Prompt yêu cầu ưu tiên dữ kiện được sửa ở lượt mới nhất và giữ đúng kiểu JSON của tham số.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | Baseline với prompt và YAML gốc | Đo hành vi ban đầu | — | 45% | [Run v0](../../starter_v0/runs/v0_B_base_openrouter_20261110T185140539504.json) |
| v1 | System prompt | Quy tắc hành động rõ sẽ giảm gọi tool thừa và đoán dữ kiện. | 45% | 70% | [Run v1](../../starter_v0/runs/v1_B_base_openrouter_20261110T185436626437.json) |
| v0-local | Baseline trên Ollama | Đo lại cấu hình gốc trên model dùng sau khi cloud hết quota. | — | 15% | [Run v0-local](../../starter_v0/runs/v0-local_B_base_ollama_20261110T190141024383.json) |
| v1-local | System prompt trên Ollama | Kiểm tra quy tắc hành động v1 trên cùng model local. | 15% | 15% | [Run v1-local](../../starter_v0/runs/v1-local_B_base_ollama_20261110T190305548398.json) |
| v2 | Mô tả tool gốc | Mô tả cụ thể về routing và args sẽ giúp model phân biệt các tool dễ nhầm. | 15% | 30% | [Run v2](../../starter_v0/runs/v2_B_base_ollama_20261110T190444602025.json) |
| v3 | System prompt | Quy tắc routing ngắn kèm ví dụ sẽ giúp model local chọn tool và giữ ngữ cảnh tốt hơn. | 30% | 50% | [Run v3](../../starter_v0/runs/v3_B_base_ollama_20261110T190656563598.json) |
| v3-integrated | YAML đầy đủ và giới hạn phản hồi Ollama | Đo cấu hình dùng trong demo sau khi tích hợp tool mới. | 50% | 40% | [Run base tích hợp](../../starter_v0/runs/v3-integrated_B_base_ollama_20261110T191634426601.json) |

Các vòng v2 và v3 dùng cùng tập tool gốc để đo riêng thay đổi prompt. Lượt base tích hợp dùng cả `dedupe_sources` và giới hạn sinh 1.024 token. Lượt này đo đủ 20 case, pass 8, nên mức giảm không thể quy cho riêng tool mới.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | Sai giá trị args | `lookup(query="AI news today")` | Đưa thời gian và loại nguồn vào từ khóa chủ đề. | Tách chủ đề, `topic` và `timeframe` trong mô tả `lookup`. |
| R06_timeframe_arg | Sai giá trị args | `lookup(topic="general")` | Dùng `general` cho yêu cầu tin công nghệ. | Quy định `topic="news"` cho tin tức. |
| R08_out_of_scope | Ngoài phạm vi | `lookup` | Gọi web để giải tích phân. | Giới hạn phạm vi research. |
| R10_missing_handle | Thiếu dữ kiện | `timeline(screenname="sama")` | Đoán tài khoản khi người dùng chưa cung cấp. | Hỏi bằng `clarify`. |
| R11_missing_url | Thiếu dữ kiện | `lookup` | Tự thay bài viết chưa có URL bằng tìm kiếm khác. | Hỏi URL bằng `clarify`. |
| R12_confirm_before_send | Sai ranh giới xác nhận | `lookup` | Tra cứu tin tức thay vì hỏi xác nhận bản tin. | Dùng `clarify(response_type="yes_no")` trước khi gửi. |
| R13_parallel_web_and_tweets | Thiếu tool | `social_search` | Thiếu `lookup` dù người dùng yêu cầu cả web lẫn X. | Cho phép nhiều tool độc lập trong cùng yêu cầu. |
| R14_out_of_scope_coding | Ngoài phạm vi | `send(confirmed=true)` | Gọi gửi khi người dùng chỉ nhờ viết code. Tool trả lỗi và không gửi. | Kiểm tra phạm vi và yêu cầu xác nhận nội dung ở lượt sau. |
| M02_carryover_timeframe | Sai giá trị args | `lookup(query="robotics news today")` | Thêm thời gian vào chủ đề đã được xác định. | Truyền thời gian qua `timeframe`. |
| M03_correction_handle | Sai giá trị args | `timeline(screenname="AndrejKarpathy")` | Ghép tên hiển thị thay vì dùng handle chính xác. | Làm rõ quy ước handle. |
| M05_correction_limit | Sai giá trị args | `timeline(limit=10)` | Dùng số cũ dù người dùng đã giảm xuống 3. | Ưu tiên điều chỉnh mới nhất và giữ các ràng buộc còn hiệu lực. |

Ở v1, routing tăng từ 70% lên 90% và độ chính xác tham số tăng từ 45% lên 70%. Hai case thiếu dữ kiện và hai case ngoài phạm vi đã pass. `R12_confirm_before_send` chuyển sang gọi `clarify`, nhưng vẫn chọn `text` thay vì `yes_no`. [Run v1](../../starter_v0/runs/v1_B_base_openrouter_20261110T185436626437.json)

Trên Ollama, cùng thay đổi v1 tăng routing từ 20% lên 25%, nhưng số case pass vẫn là 3/20. Model còn nhầm tìm trên X với tra cứu web, dùng `format` khi chưa có nguồn, và đôi khi truyền số lượng dưới dạng chuỗi. [Run v1-local](../../starter_v0/runs/v1-local_B_base_ollama_20261110T190305548398.json)

V2 sửa được việc đọc URL cụ thể và chọn `topic="news"` trong case tin công nghệ. Routing tăng từ 25% lên 40%. Các case hỏi bài của một người vẫn hay bị chuyển sang tìm theo từ khóa, và `lookup` còn gộp thời gian vào `query`. Đây là hai lỗi mà quy tắc và ví dụ của v3 nhắm tới. [Run v2](../../starter_v0/runs/v2_B_base_ollama_20261110T190444602025.json)

V3 tăng routing từ 40% lên 60% và multi-turn từ 1/6 lên 3/6. Case tìm cả web lẫn X và case đổi số bài đều pass. Model vẫn đoán sai một số handle, hỏi lại dù có URL trong R04 và chọn `send` ở R12. R12 trả `needs_confirmation`, nên lời gọi đó không gửi được. [Run v3](../../starter_v0/runs/v3_B_base_ollama_20261110T190656563598.json)

### B3. Team Eval Cases

Bộ nhóm gồm 5 case một lượt và 5 case nhiều lượt. Run đo đủ **10/10**, pass **5/10**, routing đúng **6/10** và multi-turn đúng **3/5**. [Bộ eval nhóm](../../starter_v0/data/eval_group.json) · [Run group](../../starter_v0/runs/v3_B_group_ollama_20261110T191412574874.json)

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G-S01-dedupe-sources | Gộp URL trùng từ danh sách có sẵn | `dedupe_sources` | PASS. Từ 3 mục còn 2 nguồn, bỏ 1 mục trùng. |
| G-S02-internal-privacy | Giới hạn nguồn vào policy nội bộ | `policy(policy_area="data_privacy")` | PASS. |
| G-S03-monthly-news-limit | Phạm vi tháng và số kết quả | `lookup(topic="news", timeframe="month", max_results=3)` | FAIL. Thiếu `max_results`. |
| G-S04-planning-only | Lên dàn ý trước khi tra cứu | Trả lời trực tiếp | FAIL. Gọi `lookup`, `social_search` và `policy`. |
| G-S05-missing-handle | Thiếu handle X | `clarify(response_type="text")` | FAIL. Gọi `timeline` với handle rỗng. |
| G-M01-change-social-order | Đổi thứ tự và giữ chủ đề, số lượng | `social_search(search_type="Latest", limit=2)` | PASS theo routing và args. |
| G-M02-replace-url | URL mới ghi đè URL cũ | `fetch` đúng URL mới | PASS. |
| G-M03-revised-draft-needs-confirmation | Bản tin sửa lại cần xác nhận | `clarify(response_type="yes_no")` | FAIL. Thiếu tool call. |
| G-M04-cancel-request | Người dùng từ chối gửi | Trả lời trực tiếp | FAIL. Gọi `send` dù đã hủy. Tool trả `needs_confirmation`. |
| G-M05-format-existing-items | Định dạng các nguồn từ lượt trước | `format(template="bullets")` | PASS theo routing và args cần chấm. Khi thực thi, tham số dư `description` gây `TypeError`. |

### B4. Live Chat Evidence

Chat live dùng prompt v3 và YAML tích hợp tool mới. Lượt 1 và 3 đều có lời gọi lặp được bỏ qua và có câu trả lời tổng hợp. [Transcript 4 lượt](../../starter_v0/transcripts/v3_ollama_20261110T191413259029.transcript.json)

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tìm 2 tin về pin thể rắn | `lookup` | v3 tích hợp | Tavily trả dữ liệu. Agent trả lời sau một lần gọi, nhưng liệt kê 4 tin và chỉ dẫn tên miền. |
| 2 | Tóm tắt bài chưa có URL | `clarify` với `text` | v3 tích hợp | Hỏi URL và chờ người dùng. |
| 3 | Cung cấp URL Python Tutorial | `fetch` | v3 tích hợp | Firecrawl đọc đúng URL, agent tóm tắt và dẫn link. |
| 4 | Xin xác nhận bản nháp Telegram | `clarify` với `yes_no` | v3 tích hợp | Agent chờ trả lời và không gọi `send`. Nội dung hỏi chỉ lặp lại bản nháp. |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| `dedupe_sources` | [Implementation](../../starter_v0/tools/dedupe_sources/tool.py) | Giữ nguồn đầu tiên và đếm số mục bỏ trùng. | Chỉ xử lý dữ liệu đã có trong bộ nhớ. |
| Unit test tool mới | [Tests](../../starter_v0/tests/test_tools_todo.py) | 3 test cho tool mới và 3 test hồi quy chat pass. Toàn suite có 73 pass, 14 skip từ starter. | Test chat kiểm tra bỏ lời gọi trùng, chặn tool ngoài danh sách và xử lý args dư rỗng. Eval nhóm đo lựa chọn của model. |
| UI | [app.py](../../starter_v0/app.py) và [link dùng thử](https://cordless-excess-sys-friend.trycloudflare.com) | AppTest với Ollama thật đã xác nhận UI hỏi URL và chờ trả lời. Trang public trả HTTP 200 và WebSocket kết nối được. | Demo Telegram chỉ xem trước. Tunnel cần máy demo đang chạy. |

### B5. Bonus Evidence

Phần bằng chứng chấm điểm chính nằm ở B1–B5a.

### B7. Small Local Model Challenge (bonus)

Nhóm dùng một model local, `llama3.2:3b`, để tiếp tục các vòng eval chính sau khi hết quota OpenRouter. Các mốc so sánh cùng model nằm ở B1.

## 5. Khó khăn và cách xử lý

- Preflight qua OpenRouter trả HTTP 402 với model mặc định và HTTP 429 với `google/gemma-4-31b-it:free`. `nvidia/nemotron-3.5-lightning:free` đo đủ 20 case trong baseline. Baseline sử dụng bản sao prompt và YAML gốc lưu trước khi đăng ký tool mới.
- OpenRouter dừng ở case R13 khi chạy v2 với HTTP 429 do hết hạn mức model miễn phí trong ngày. Lượt chạy dở không dùng làm bằng chứng điểm. Các phiên bản sau được đo lại trên cùng model Ollama để kiểm soát biến model.
- Smoke test Tavily và Firecrawl trả dữ liệu thật. Twitter API45 trả HTTP 403 với thông báo key chưa đăng ký API. Một lượt thử `social_search` trả HTTP 429. Runner chấm routing và tham số riêng với lỗi chạy tool, nên các lỗi này vẫn cần đối chiếu trong `tool_results`.
- Chat thử v3 lặp cùng một lời gọi `lookup` hoặc `fetch` tới giới hạn vòng lặp. Vòng lặp chat hiện bỏ qua lời gọi trùng trong một lượt và yêu cầu model tổng hợp từ dữ liệu đã nhận khi không có lời gọi mới. [Transcript tái hiện lỗi](../../starter_v0/transcripts/v3_ollama_20261110T190602453839.transcript.json)
- Khi thử UI, model thêm trường rỗng như `url=""` vào `clarify`. Vòng lặp chat giữ args gốc trong log và bỏ trường lạ có giá trị rỗng trước khi chạy tool. Runner eval vẫn chấm lời gọi gốc.
- Hai yêu cầu Ollama chạy kéo dài trong lần thử group và chat song song. Lượt chạy lại theo thứ tự và giới hạn phản hồi local ở 1.024 token. Các run base v0-local đến v3 giữ cấu hình sinh ban đầu để so sánh.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Prompt quy định hành động theo ngữ cảnh, ưu tiên thông tin mới nhất và yêu cầu xác nhận trước khi gửi. YAML giải thích input cụ thể của từng tool, chẳng hạn handle bỏ `@` và thời gian truyền qua `timeframe`.
- Cần đọc `tool_results` để phát hiện API lỗi dù routing được chấm đúng. Với yêu cầu gửi, cần đối chiếu transcript để biết agent đã hỏi và dừng chờ người dùng hay chưa.
- Một vòng tiếp theo có thể thử tách bước xác định handle khỏi bước lấy timeline, rồi đo xem có giảm lỗi handle ở R01 và M03 mà không phát sinh lời gọi thừa hay không.

## 8. Tài liệu tham khảo

- [Đề bài](../../README.md)
- [Hướng dẫn cấu hình](../../docs/TOOL-SETUP.md)
- [Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/)
