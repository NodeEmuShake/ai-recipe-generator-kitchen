"""Meal-plan service — composes multiple recipe generations into a plan."""
from __future__ import annotations

import logging
from datetime import date, timedelta

from kitchen.config.settings import Settings
from kitchen.models.meal_plan import MealPlan, DayPlan
from kitchen.services.model_registry import ModelRegistry
from kitchen.services.recipe_service import RecipeService

log = logging.getLogger("kitchen.plan")

_MEALS = ("breakfast", "lunch", "dinner")


class MealPlanService:
    def __init__(self, settings: Settings, registry: ModelRegistry) -> None:
        self.settings = settings
        self.recipes = RecipeService(settings, registry)

    def plan(self, days: int, model_id: str | None = None) -> MealPlan:
        plan = MealPlan(dietary_profile=self.settings.dietary_profile)
        today = date.today()
        for offset in range(days):
            day = DayPlan(day=(today + timedelta(days=offset)).isoformat())
            for meal in _MEALS:
                try:
                    rec = self.recipes.generate(
                        ingredients=[f"a {meal} suitable for {self.settings.dietary_profile}"],
                        model_id=model_id,
                    )
                    setattr(day, meal, rec)
                except Exception:
                    log.exception("failed to plan %s for %s", meal, day.day)
            plan.days.append(day)
        return plan