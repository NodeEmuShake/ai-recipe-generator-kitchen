"""Model registry — discovers installed weights on disk and reports metadata."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ModelEntry:
    id: str
    path: Path
    quant: str
    size_mb: float


class ModelRegistry:
    """Scans `models_dir` for `*.gguf` files and derives ids from filenames.

    Filename convention: `<id>.<quant>.gguf`, e.g. `pantry-lite-3b.Q4_K_M.gguf`.
    """

    def __init__(self, models_dir: Path) -> None:
        self.models_dir = models_dir
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def list_installed(self) -> list[ModelEntry]:
        entries: list[ModelEntry] = []
        for path in sorted(self.models_dir.glob("*.gguf")):
            stem = path.stem
            if "." in stem:
                model_id, quant = stem.rsplit(".", 1)
            else:
                model_id, quant = stem, "unknown"
            entries.append(ModelEntry(
                id=model_id,
                path=path,
                quant=quant,
                size_mb=path.stat().st_size / (1024 * 1024),
            ))
        return entries

    def resolve(self, model_id: str) -> ModelEntry:
        for entry in self.list_installed():
            if entry.id == model_id:
                return entry
        raise FileNotFoundError(f"model '{model_id}' not installed in {self.models_dir}")