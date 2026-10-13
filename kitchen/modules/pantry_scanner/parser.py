"""Parse free-form pantry text into normalized ingredient names."""
from __future__ import annotations

import re

_NOISE = re.compile(r"\(.*?\)|\[.*?\]")
_QTY_PREFIX = re.compile(r"^\s*[\d./]+\s*[a-zA-Z]*\s+")


def normalize(line: str) -> str | None:
    line = _NOISE.sub("", line).strip()
    if not line or line.startswith("#"):
        return None
    line = _QTY_PREFIX.sub("", line)
    return line.lower().strip(" ,.;:")


def parse_pantry(text: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in text.splitlines():
        item = normalize(raw)
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out