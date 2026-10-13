"""Deterministic plating notes keyed off recipe tags. No model call."""
from __future__ import annotations

from kitchen.models.recipe import Recipe

_NOTES = {
    "soup": "Serve in a warmed bowl; finish with a swirl of oil and cracked pepper.",
    "salad": "Chill plates 10 minutes before plating; dress at the last second.",
    "roast": "Rest 8 minutes under foil; carve against the grain.",
    "pasta": "Reserve a cup of pasta water; toss off-heat to emulsify.",
    "dessert": "Plate with a quenelle of cream; dust with cocoa at the table.",
    "breakfast": "Warm the plates; hold in a low oven if serving staggered.",
}


def suggest(recipe: Recipe) -> str:
    for tag in recipe.tags:
        note = _NOTES.get(tag.lower().strip())
        if note:
            return note
    return "Plate simply; let the food speak."