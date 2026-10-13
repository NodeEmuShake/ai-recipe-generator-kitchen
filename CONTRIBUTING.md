# Contributing to ai-recipe-generator-kitchen

Thanks for wanting to help. This is a hobbyist, offline-first project —
we ship features that work on a laptop with no network access.

## Setup

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Model weights are not bundled. Drop a GGUF into
`%APPDATA%\ai-recipe-generator-kitchen\models\` named
`<id>.<quant>.gguf` (e.g. `pantry-lite-3b.Q4_K_M.gguf`).

## Layout

- `kitchen/bootstrap.py` — entry point, argument parsing.
- `kitchen/config/` — settings and platform paths.
- `kitchen/models/` — dataclasses for recipes, plans, prompts.
- `kitchen/handlers/` — CLI and stream handlers.
- `kitchen/services/` — orchestration and the inference engine.
- `kitchen/lib/` — pure functions; no I/O, easy to test.
- `kitchen/modules/` — feature modules (pantry scanner, dietary filter, plating).
- `kitchen/utils/` — small helpers.

## Style

- Python 3.11+. Ruff for lint, mypy for types.
- No network calls in `kitchen.lib.*` or `kitchen.modules.*`.
- New services go under `kitchen/services/`; new pure logic under `kitchen/lib/`.

## Tests

```powershell
pytest -q
ruff check .
mypy kitchen
```

## Pull requests

One feature per