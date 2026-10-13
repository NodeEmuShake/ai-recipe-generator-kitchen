"""Inference engine — thin wrapper over llama-cpp-python.

Watch for the KV-cache growth in llama-cpp-python <0.2.70: long generations
on 3B models can push past 4GB RSS. We reload per call rather than cache
the context, which is slower (~1.2s cold) but bounded.
"""
from __future__ import annotations

import logging
from collections.abc import Iterator

from kitchen.config.settings import Settings
from kitchen.models.prompt import PromptEnvelope, CompletionEnvelope
from kitchen.services.model_registry import ModelRegistry

log = logging.getLogger("kitchen.engine")


class InferenceEngine:
    def __init__(self, settings: Settings, registry: ModelRegistry) -> None:
        self.settings = settings
        self.registry = registry

    def _load(self, model_id: str):
        try:
            from llama_cpp import Llama
        except ImportError as exc:
            raise RuntimeError(
                "llama-cpp-python is not installed. Run: pip install llama-cpp-python"
            ) from exc
        entry = self.registry.resolve(model_id)
        log.info("loading %s (%s, %.1f MB)", entry.id, entry.quant, entry.size_mb)
        return Llama(
            model_path=str(entry.path),
            n_ctx=4096,
            n_threads=4,
            verbose=False,
        )

    def run(self, prompt: PromptEnvelope, model_id: str) -> CompletionEnvelope:
        llm = self._load(model_id)
        out = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
            temperature=prompt.temperature,
            top_p=self.settings.top_p,
            max_tokens=prompt.max_tokens,
            stop=prompt.stop or None,
        )
        choice = out["choices"][0]
        usage = out.get("usage", {})
        return CompletionEnvelope(
            text=choice["message"]["content"],
            model_id=model_id,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            finish_reason=choice.get("finish_reason", "stop"),
        )

    def stream(self, prompt: PromptEnvelope, model_id: str) -> Iterator[str]:
        llm = self._load(model_id)
        for chunk in llm.create_chat_completion(
            messages=[
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
            temperature=prompt.temperature,
            top_p=self.settings.top_p,
            max_tokens=prompt.max_tokens,
            stream=True,
        ):
            delta = chunk["choices"][0].get("delta", {})
            if "content" in delta:
                yield delta["content"]