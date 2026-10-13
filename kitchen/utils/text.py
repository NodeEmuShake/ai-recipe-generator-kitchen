"""Small text helpers used across the toolkit."""
from __future__ import annotations

import re

_WS_RE = re.compile(r"[ \t]+")


def slugify(text: str) -> str:
    text = _WS_RE.sub(" ", text.strip().lower())
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def truncate(text: str, limit: int = 200, ellipsis: str = "…") -> str:
    return text if len(text) <= limit else text[: limit - len(ellipsis)] + ellipsis