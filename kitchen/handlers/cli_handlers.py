"""Dispatch parsed CLI commands to the appropriate service."""
from __future__ import annotations

import argparse
import json
import logging
import sys

from kitchen.config.settings import Settings
from kitchen.services.model_registry import ModelRegistry
from kitchen.services.recipe_service import RecipeService
from kitchen.services.meal_plan_service import MealPlanService
from kitchen.services.substitution_service import SubstitutionService

log = logging.getLogger("kitchen.cli")


def _read_lines(prompt: str) -> list[str]:
    print(prompt, file=sys.stderr)
    return [line.strip() for line in sys.stdin if line.strip()]


def dispatch(args: argparse.Namespace, settings: Settings, registry: ModelRegistry) -> int:
    if args.command == "generate":
        ingredients = _read_lines("Enter ingredients, one per line (Ctrl-Z then Enter on Windows):")
        svc = RecipeService(settings, registry)
        recipe = svc.generate(ingredients, model_id=args.model)
        print(json.dumps(recipe.to_dict(), indent=2))
        return 0

    if args.command == "plan":
        days = int(input("How many days? ").strip() or "3")
        svc = MealPlanService(settings, registry)
        plan = svc.plan(days, model_id=args.model)
        print(json.dumps([d.__dict__ for d in plan.days], indent=2, default=str))
        return 0

    if args.command == "substitute":
        target = input("Ingredient to substitute: ").strip()
        svc = SubstitutionService(settings, registry)
        for option in svc.suggest(target, model_id=args.model):
            print(f"- {option}")
        return 0

    log.error("unknown command: %s", args.command)
    return 2