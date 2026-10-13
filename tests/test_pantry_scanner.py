"""Pantry scanner tests."""
from __future__ import annotations

from kitchen.modules.pantry_scanner.parser import parse_pantry


def test_strips_quantities_and_noise():
    text = """
    2 lb chicken thighs (boneless)
    # a comment
    500g potatoes
    3 cloves garlic
    chicken thighs
    """
    assert parse_pantry(text) == ["chicken thighs", "potatoes", "garlic"]


def test_empty_input():
    assert parse_pantry("") == []