"""Platform-aware data directory resolution (Windows-first, POSIX fallback)."""
from __future__ import annotations

import os
from pathlib import Path


def resolve_data_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        root = base / "ai-recipe-generator-kitchen"
    else:
        root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "kitchen"
    root.mkdir(parents=True, exist_ok=True)
    return root