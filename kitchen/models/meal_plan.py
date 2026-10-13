"""Multi-day meal plan model."""
from __future__ import annotations

from dataclasses import dataclass, field

from kitchen.models.recipe import Recipe


@dataclass(slots=True)
class DayPlan:
    day: str
    breakfast: Recipe | None = None
    lunch: Recipe | None = None
    dinner: Recipe | None = None

    def all_recipes(self) -> list[Recipe]:
        return [r for r in (self.breakfast, self.lunch, self.dinner) if r is not None]


@dataclass(slots=True)
class MealPlan:
    days: list[DayPlan] = field(default_factory=list)
    dietary_profile: str = "omnivore"

    def total_recipes(self) -> int:
        return sum(len(d.all_recipes()) for d in self.days)