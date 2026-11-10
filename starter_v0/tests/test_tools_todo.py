"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from chat import execute_tool_call, run_model_tool_loop
from conftest import FakeResponse
from providers.base import ModelResponse, ToolCall
from tools import TOOL_FUNCTIONS

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

def test_dedupe_sources_keeps_first_item_and_preserves_distinct_queries() -> None:
    first = {"url": "https://EXAMPLE.org/report?v=1#intro", "title": "First source"}
    duplicate = {"url": "https://example.org/report?v=1#details", "title": "Duplicate"}
    other = {"url": "https://example.org/report?v=2", "title": "Different source"}

    result = TOOL_FUNCTIONS["dedupe_sources"]([first, duplicate, other])

    assert result == {
        "tool": "dedupe_sources",
        "items": [first, other],
        "input_count": 3,
        "unique_count": 2,
        "removed_count": 1,
    }


def test_dedupe_sources_rejects_non_list_input() -> None:
    result = TOOL_FUNCTIONS["dedupe_sources"]("https://example.org/report")

    assert result["error"] == "ValueError"
    assert "list" in result["message"]


def test_dedupe_sources_returns_error_for_malformed_url() -> None:
    result = TOOL_FUNCTIONS["dedupe_sources"]([
        {"url": "https://example.org/report"},
        {"url": "https://[invalid/report"},
    ])

    assert result["error"] == "ValueError"
    assert "items" not in result


def test_chat_answers_after_repeated_lookup_without_repeating_http(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "fake")
    requests = fake_http(FakeResponse({"results": []}))

    class RepeatingProvider:
        def complete(self, messages, tools, **kwargs):
            if tools:
                return ModelResponse(tool_calls=[ToolCall("lookup", {"query": "robotics"})])
            assert "TOOL_RESULTS_JSON" in str(messages)
            return ModelResponse(text="No matching sources.")

    result = run_model_tool_loop(
        provider=RepeatingProvider(),
        messages=[{"role": "user", "content": "Find sources about robotics."}],
        tools=[{"type": "function", "function": {"name": "lookup"}}],
        model=None,
        max_tool_rounds=4,
    )

    assert len(requests) == 1
    assert result["status"] == "answered"
    assert result["assistant_text"] == "No matching sources."
    assert result["rounds"][1]["tool_results"][0]["result"]["status"] == "duplicate_call_skipped"


def test_chat_does_not_execute_unavailable_send_tool(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "fake")
    requests = fake_http(FakeResponse())

    class Provider:
        def complete(self, messages, tools, **kwargs):
            if messages[-1]["role"] == "system":
                return ModelResponse(tool_calls=[ToolCall("send", {"text": "Draft", "confirmed": True})])
            return ModelResponse(text="Preview only.")

    result = run_model_tool_loop(
        provider=Provider(),
        messages=[{"role": "system", "content": "Telegram preview."}],
        tools=[{"type": "function", "function": {"name": "clarify"}}],
        model=None,
        max_tool_rounds=2,
    )

    assert requests == []
    assert result["tool_events"][0]["result"]["error"] == "tool_not_available"


def test_chat_accepts_clarify_when_model_adds_empty_unknown_arguments() -> None:
    call = ToolCall("clarify", {
        "question": "Bạn gửi URL được không?",
        "response_type": "text",
        "url": "",
        "max_results": None,
    })

    event = execute_tool_call(call)

    assert event["args"] == call.args
    assert event["result"]["awaiting_user"] is True
    assert event["result"]["question"] == call.args["question"]
