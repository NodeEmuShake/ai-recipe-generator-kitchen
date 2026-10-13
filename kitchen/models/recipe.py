"""Recipe domain model."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(slots=True)
class Ingredient:
    name: str
    quantity: float
    unit: str
    optional: bool = False
    substitutions: list[str] = field(default_factory=list)

    def scaled(self, factor: float) -> "Ingredient":
        return Ingredient(
            name=self.name,
            quantity=round(self.quantity * factor, 3),
            unit=self.unit,
            optional=self.optional,
            substitutions=list(self.substitutions),
        )


@dataclass(slots=True)
class Recipe:
    title: str
    servings: int
    ingredients: list[Ingredient]
    steps: list[str]
    prep_minutes: int
    cook_minutes: int
    tags: list[str] = field(default_factory=list)
    model_id: str = ""

    @property
    def total_minutes(self) -> int:
        return self.prep_minutes + self.cook_minutes

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)