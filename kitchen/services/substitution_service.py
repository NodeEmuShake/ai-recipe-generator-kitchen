"""Substitution service — suggests swaps for a given ingredient."""
from __future__ import annotations

from kitchen.config.settings import Settings
from kitchen.lib.prompt_builder import build_substitution_prompt
from kitchen.services.model_registry import ModelRegistry
from kitchen.services.inference_engine import InferenceEngine


class SubstitutionService:
    def __init__(self, settings: Settings, registry: ModelRegistry) -> None:
        self.settings = settings
        self.engine = InferenceEngine(settings, registry)

    def suggest(self, ingredient: str, model_id: str | None = None) -> list[str]:
        prompt = build_substitution_prompt(
            ingredient=ingredient,
            dietary=self.settings.dietary_profile,
        )
        completion = self.engine.run(prompt, model_id=model_id or self.settings.default_model)
        return [line.strip("-• \t") for line in completion.text.splitlines() if line.strip()]