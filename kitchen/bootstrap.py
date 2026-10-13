"""Application bootstrap — wires config, model registry, and the CLI dispatcher."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from kitchen.config.settings import load_settings
from kitchen.config.paths import resolve_data_dir
from kitchen.services.model_registry import ModelRegistry
from kitchen.handlers.cli_handlers import dispatch


def _configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s :: %(message)s",
        datefmt="%H:%M:%S",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kitchen",
        description="AI recipe generator — on-device, offline-first.",
    )
    parser.add_argument("--config", type=Path, default=None,
                        help="Path to kitchen.toml (defaults to %%APPDATA%%/ai-recipe-generator-kitchen).")
    parser.add_argument("--model", default="pantry-lite-3b",
                        help="Model id from the registry, e.g. pantry-lite-3b.")
    parser.add_argument("--offline", action="store_true",
                        help="Refuse any network call; use only local weights.")
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("generate", help="Generate a recipe from an ingredient list.")
    sub.add_parser("plan", help="Generate a multi-day meal plan.")
    sub.add_parser("substitute", help="Suggest ingredient substitutions.")
    sub.add_parser("list-models", help="List installed model weights.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _configure_logging("DEBUG" if args.verbose else "INFO")

    data_dir = resolve_data_dir()
    settings = load_settings(args.config, data_dir)
    registry = ModelRegistry(settings.models_dir)

    if args.command == "list-models":
        for entry in registry.list_installed():
            print(f"{entry.id:<24} {entry.quant:<8} {entry.size_mb:>7.1f} MB")
        return 0

    return dispatch(args, settings, registry)


if __name__ == "__main__":
    sys.exit(main())