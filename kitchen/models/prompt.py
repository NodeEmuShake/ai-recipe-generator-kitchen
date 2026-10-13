"""Prompt and completion envelopes passed between handlers and engines."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PromptEnvelope:
    system: str
    user: str
    stop: list[str] = field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 1024


@dataclass(slots=True)
class CompletionEnvelope:
    text: str
    model_id: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    finish_reason: str = "stop"