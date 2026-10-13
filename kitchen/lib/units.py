"""Unit conversion — metric <-> imperial, plus volume normalization."""
from __future__ import annotations

_ML_PER = {
    "ml": 1.0, "l": 1000.0, "tsp": 4.92892, "tbsp": 14.7868,
    "cup": 236.588, "floz": 29.5735, "pint": 473.176, "quart": 946.353,
}

_G_PER = {
    "g": 1.0, "kg": 1000.0, "oz": 28.3495, "lb": 453.592,
}


def to_ml(quantity: float, unit: str) -> float:
    key = unit.lower().rstrip(".")
    if key not in _ML_PER:
        raise KeyError(f"unknown volume unit: {unit}")
    return quantity * _ML_PER[key]


def to_grams(quantity: float, unit: str) -> float:
    key = unit.lower().rstrip(".")
    if key not in _G_PER:
        raise KeyError(f"unknown mass unit: {unit}")
    return quantity * _G_PER[key]