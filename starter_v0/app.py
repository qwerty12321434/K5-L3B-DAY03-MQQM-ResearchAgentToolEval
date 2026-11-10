from __future__ import annotations

import os

import streamlit as st

from chat import ARTIFACTS_DIR, run_model_tool_loop, trim_history
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools


UI_POLICY = (
    "The Streamlit demo previews Telegram posts only. "
    "For a request to publish, use clarify with response_type=yes_no and the draft to review. "
    "If the user confirms, explain that this demo cannot publish."
)


def render_assistant(message: dict) -> None:
    with st.chat_message("assistant"):
        st.markdown(message["content"])
        events = message.get("tool_events", [])
        if events:
            with st.expander("Hoạt động của tool"):
                for event in events:
                    name = event["tool"]
                    result = event["result"]
                    if "error" in result:
                        st.error(f"{name} · {result['error']}")
                    else:
                        st.write(f"{name} · {result.get('status', 'đã chạy')}")


def main() -> None:
    st.set_page_config(page_title="Research Agent", page_icon="🔎")
    st.title("Research Agent")
    st.caption("Tìm nguồn, đọc URL và tổng hợp bản tin. Telegram chỉ hỗ trợ xem trước.")

    messages = st.session_state.setdefault("messages", [])
    for message in messages:
        if message["role"] == "assistant":
            render_assistant(message)
        else:
            with st.chat_message("user"):
                st.write(message["content"])

    provider_name = os.getenv("RESEARCH_PROVIDER", "openrouter")
    if provider_name not in {"openrouter", "ollama"}:
        st.error("RESEARCH_PROVIDER phải là openrouter hoặc ollama.")
        return

    ready = provider_name == "ollama" or bool(os.getenv("OPENROUTER_API_KEY", "").strip())
    if not ready:
        st.warning("Điền OPENROUTER_API_KEY vào starter_v0/.env rồi khởi động lại Streamlit.")

    query = st.chat_input("Ví dụ: Tìm 3 tin mới về robot trong tuần này", disabled=not ready)
    if not query or not query.strip():
        return
    query = query.strip()
    with st.chat_message("user"):
        st.write(query)

    prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
    declarations = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
    available_tools = [tool for tool in declarations if tool["name"] != "send"]
    history = [{"role": item["role"], "content": item["content"]} for item in messages]
    try:
        with st.spinner("Agent đang xử lý yêu cầu…"):
            result = run_model_tool_loop(
                provider=make_provider(provider_name),
                messages=[
                    {"role": "system", "content": f"{prompt}\n\n{UI_POLICY}"},
                    *trim_history(history, 5),
                    {"role": "user", "content": query},
                ],
                tools=to_openai_tools(available_tools),
                model=os.getenv(f"{provider_name.upper()}_MODEL") or None,
                max_tool_rounds=4,
            )
    except Exception as exc:
        status = getattr(exc, "status_code", None)
        detail = f"HTTP {status}" if isinstance(status, int) else type(exc).__name__
        st.error(f"Không gọi được {provider_name} ({detail}). Kiểm tra cấu hình rồi thử lại.")
        return

    assistant = {
        "role": "assistant",
        "content": result["assistant_text"] or "Agent chưa có câu trả lời cho yêu cầu này.",
        "tool_events": result["tool_events"],
    }
    messages.extend([{"role": "user", "content": query}, assistant])
    render_assistant(assistant)


if __name__ == "__main__":
    main()
