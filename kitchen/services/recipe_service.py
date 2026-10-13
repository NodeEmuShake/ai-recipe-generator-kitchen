"""Recipe generation service — orchestrates prompt building, inference, parsing."""
from __future__ import annotations

import logging

from kitchen.config.settings import Settings
from kitchen.lib.prompt_builder import build_recipe_prompt
from kitchen.lib.recipe_parser import parse_recipe
from kitchen.models.recipe import Recipe
from kitchen.services.model_registry import ModelRegistry
from kitchen.services.inference_engine import InferenceEngine

log = logging.getLogger("kitchen.recipe")


class RecipeService:
    def __init__(self, settings: Settings, registry: ModelRegistry) -> None:
        self.settings = settings
        self.registry = registry
        self.engine = InferenceEngine(settings, registry)

    def generate(self, ingredients: list[str], model_id: str | None = None) -> Recipe:
        mid = model_id or self.settings.default_model
        prompt = build_recipe_prompt(
            ingredients=ingredients,
            dietary=self.settings.dietary_profile,
            units=self.settings.units,
        )
        log.debug("prompt built: %d chars", len(prompt.user))
        completion = self.engine.run(prompt, model_id=mid)
        return parse_recipe(completion.text, model_id=mid)