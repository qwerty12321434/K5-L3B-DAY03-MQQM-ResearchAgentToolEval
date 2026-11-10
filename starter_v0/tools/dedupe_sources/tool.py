from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

from tools._shared import err


def dedupe_sources(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Keep the first source for each HTTP(S) URL, ignoring fragments."""
    tool = "dedupe_sources"
    try:
        if not isinstance(items, list):
            raise ValueError("items must be a list of source objects")

        unique_items: list[dict[str, Any]] = []
        seen_urls: set[str] = set()
        for index, item in enumerate(items):
            if not isinstance(item, dict) or not isinstance(item.get("url"), str):
                raise ValueError(f"items[{index}].url must be a string")

            url = item["url"].strip()
            parts = urlsplit(url)
            if (
                parts.scheme not in {"http", "https"}
                or not parts.hostname
                or parts.username is not None
                or any(char.isspace() or ord(char) < 32 for char in url)
            ):
                raise ValueError(f"items[{index}].url must be an absolute HTTP(S) URL without credentials")
            if parts.port == 0:
                raise ValueError(f"items[{index}].url has an invalid port")

            key = parts._replace(netloc=parts.netloc.lower(), path=parts.path or "/", fragment="").geturl()
            if key not in seen_urls:
                seen_urls.add(key)
                unique_items.append(item)

        return {
            "tool": tool,
            "items": unique_items,
            "input_count": len(items),
            "unique_count": len(unique_items),
            "removed_count": len(items) - len(unique_items),
        }
    except ValueError as exc:
        return err(tool, exc)
