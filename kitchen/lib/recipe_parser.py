"""Parse model output into a Recipe dataclass.

The parser is deliberately lenient: models drift from the requested format
under low temperature, and a hard failure here is worse than a slightly
wrong recipe. Missing sections raise; extra sections are ignored.
"""
from __future__ import annotations

import re

from kitchen.models.recipe import Ingredient, Recipe

_SECTION_RE = re.compile(
    r"^(TITLE|SERVINGS|INGREDIENTS|STEPS|TIMES|TAGS)\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_ING_RE = re.compile(r"^(?P<qty>[\d./]+)\s*(?P<unit>[a-zA-Z]+)?\s*(?P<name>.+)$")
_TIME_RE = re.compile(r"(?P<prep>\d+)\s*m?\s*prep.*?(?P<cook>\d+)\s*m?\s*cook", re.IGNORECASE)


def _split_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        m = _SECTION_RE.match(line.strip())
        if m:
            current = m.group(1).upper()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def _parse_ingredient(line: str) -> Ingredient | None:
    line = line.strip(" -*•\t")
    if not line:
        return None
    m = _ING_RE.match(line)
    if not m:
        return Ingredient(name=line, quantity=0.0, unit="")
    qty_raw = m.group("qty")
    try:
        qty = float(qty_raw)
    except ValueError:
        try:
            qty = float(eval(qty_raw, {"__builtins__": {}}))  # noqa: S307 — fractions like 1/2
        except Exception:
            qty = 0.0
    return Ingredient(name=m.group("name").strip(), quantity=qty, unit=(m.group("unit") or "").strip())


def parse_recipe(text: str, model_id: str = "") -> Recipe:
    sections = _split_sections(text)
    if "INGREDIENTS" not in sections or "STEPS" not in sections:
        raise ValueError("model output missing required sections (INGREDIENTS, STEPS)")

    ingredients = [i for i in (_parse_ingredient(l) for l in sections["INGREDIENTS"].splitlines()) if i]
    steps = [
        re.sub(r"^\s*\d+[.)]\s*", "", s).strip()
        for s in sections["STEPS"].splitlines()
        if s.strip()
    ]
    tags = [t.strip() for t in sections.get("TAGS", "").split(",") if t.strip()]

    prep, cook = 0, 0
    times = sections.get("TIMES", "")
    if m := _TIME_RE.search(times):
        prep, cook = int(m.group("prep")), int(m.group("cook"))

    try:
        servings = int(re.search(r"\d+", sections.get("SERVINGS", "4")).group())
    except (AttributeError, ValueError):
        servings = 4

    return Recipe(
        title=sections.get("TITLE", "Untitled").strip().splitlines()[0],
        servings=servings,
        ingredients=ingredients,
        steps=steps,
        prep_minutes=prep,
        cook_minutes=cook,
        tags=tags,
        model_id=model_id,
    )