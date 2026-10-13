"""Parser tests — the format is lenient, so pin the leniency."""
from __future__ import annotations

import pytest

from kitchen.lib.recipe_parser import parse_recipe

SAMPLE = """\
TITLE: Pantry Tomato Pasta
SERVINGS: 2
INGREDIENTS:
- 200 g spaghetti
- 2 tbsp olive oil
- 3 cloves garlic, minced
- 400 g canned tomatoes
STEPS:
1. Boil water and salt heavily.
2. Sauté garlic in oil until fragrant.
3. Add tomatoes, simmer 10 minutes.
4. Toss with pasta and a splash of pasta water.
TIMES: 10m prep, 20m cook
TAGS: pasta, vegetarian, weeknight
"""


def test_parses_full_recipe():
    r = parse_recipe(SAMPLE, model_id="pantry-lite-3b")
    assert r.title == "Pantry Tomato Pasta"
    assert r.servings == 2
    assert len(r.ingredients) == 4
    assert r.ingredients[0].name == "spaghetti"
    assert r.ingredients[0].quantity == 200.0
    assert r.ingredients[0].unit == "g"
    assert r.prep_minutes == 10 and r.cook_minutes == 20
    assert "pasta" in r.tags


def test_missing_ingredients_raises():
    with pytest.raises(ValueError):
        parse_recipe("TITLE: Nothing\nSTEPS:\n1. Do nothing.\n")


def test_fractional_quantity():
    text = "INGREDIENTS:\n- 1/2 cup sugar\nSTEPS:\n1. Add.\n"
    r = parse_recipe(text)
    assert r.ingredients[0].quantity == pytest.approx(0.5)