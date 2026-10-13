"""Rule tables for common dietary profiles.

These are heuristics, not medical advice. The filter warns; it does not
rewrite the recipe. Callers decide what to do with violations.
"""
from __future__ import annotations

from kitchen.models.recipe import Recipe

_FORBIDDEN: dict[str, set[str]] = {
    "vegan": {"meat", "chicken", "beef", "pork", "fish", "egg", "milk", "cheese",
              "butter", "honey", "yogurt", "cream", "gelatin"},
    "vegetarian": {"meat", "chicken", "beef", "pork", "fish", "gelatin"},
    "keto": {"sugar", "flour", "rice", "bread", "pasta", "potato", "honey"},
    "gluten-free": {"flour", "bread", "pasta", "barley", "rye", "wheat"},
}


def check(recipe: Recipe, profile: str) -> list[str]:
    forbidden = _FORBIDDEN.get(profile.lower())
    if not forbidden:
        return []
    hits: list[str] = []
    for ing in recipe.ingredients:
        name = ing.name.lower()
        for token in forbidden:
            if token in name:
                hits.append(f"{ing.name} conflicts with '{profile}' (matched '{token}')")
                break
    return hits