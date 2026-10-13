"""Typed settings loaded from kitchen.toml with sane defaults."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True, slots=True)
class Settings:
    models_dir: Path
    cache_dir: Path
    default_model: str = "pantry-lite-3b"
    temperature: float = 0.7
    top_p: float = 0.92
    max_tokens: int = 1024
    offline: bool = True
    dietary_profile: str = "omnivore"
    units: str = "metric"


DEFAULTS = Settings(
    models_dir=Path.home() / ".kitchen" / "models",
    cache_dir=Path.home() / ".kitchen" / "cache",
)


def load_settings(config_path: Path | None, data_dir: Path) -> Settings:
    if config_path is None or not config_path.exists():
        return DEFAULTS
    with config_path.open("rb") as fh:
        raw = tomllib.load(fh)
    section = raw.get("kitchen", {})
    return Settings(
        models_dir=Path(section.get("models_dir", data_dir / "models")),
        cache_dir=Path(section.get("cache_dir", data_dir / "cache")),
        default_model=section.get("default_model", DEFAULTS.default_model),
        temperature=float(section.get("temperature", DEFAULTS.temperature)),
        top_p=float(section.get("top_p", DEFAULTS.top_p)),
        max_tokens=int(section.get("max_tokens", DEFAULTS.max_tokens)),
        offline=bool(section.get("offline", DEFAULTS.offline)),
        dietary_profile=section.get("dietary_profile", DEFAULTS.dietary_profile),
        units=section.get("units", DEFAULTS.units),
    )