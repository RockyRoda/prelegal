"""Access to the root templates/ directory holding the raw document markdown."""

import os
from pathlib import Path

_DEFAULT_TEMPLATES_DIR = Path(__file__).resolve().parents[3] / "templates"


def get_templates_dir() -> Path:
    return Path(os.environ.get("PRELEGAL_TEMPLATES_DIR", _DEFAULT_TEMPLATES_DIR))


def read_template(filename: str) -> str:
    return (get_templates_dir() / filename).read_text(encoding="utf-8")
