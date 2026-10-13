"""Prompt construction for the recipe generator."""
from __future__ import annotations

from kitchen.models.prompt import PromptEnvelope

SYSTEM = (
    "You are a precise recipe generator. Emit recipes as plain text with the "
    "following sections in order: TITLE, SERVINGS, INGREDIENTS, STEPS, TIMES, TAGS. "
    "Ingredients must be one per line as '<qty> <unit> <name>'. Steps must be "
    "numbered. Times must be '<prep>m prep, <cook>m cook'. TAGS is a comma list. "
    "Never invent allergens. Respect the dietary profile strictly."
)


def build_recipe_prompt(ingredients: list[str], dietary: str, units: str) -> PromptEnvelope:
    joined = "\n".join(f"- {i}" for i in ingredients) or "- (anything in a pantry)"
    user = (
        f"Dietary profile: {dietary}\n"
        f"Units: {units}\n"
        f"Available ingredients:\n{joined}\n\n"
        "Generate one recipe using primarily these ingredients."
    )
    return PromptEnvelope(system=SYSTEM, user=user, stop=["</recipe>"])


def build_substitution_prompt(ingredient: str, dietary: str) -> PromptEnvelope:
    user = (
        f"Suggest 3 to 5 substitutes for '{ingredient}' that fit a {dietary} diet. "
        "Return one per line, no numbering."
    )
    return PromptEnvelope(system=SYSTEM, user=user, stop=["\n\n\n"])