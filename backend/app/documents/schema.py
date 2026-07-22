"""Data model describing a catalog document's fillable fields.

Field values are collected as plain strings via chat and substituted into the
document's real template markdown - see render.py. A field is either a
"defined term" (a role name like Customer/Provider that stays literal in the
body and is only mapped to its real value on a generated summary table) or
"substituted" (its matching span text is replaced with the real value
everywhere it appears in the body, like Governing Law or Effective Date).
"""

from dataclasses import dataclass
from enum import Enum


class FieldKind(str, Enum):
    STRING = "string"
    DATE = "date"
    ENUM = "enum"


class FieldRole(str, Enum):
    DEFINED_TERM = "defined_term"
    SUBSTITUTED = "substituted"
    SUMMARY_ONLY = "summary_only"


@dataclass(frozen=True)
class FieldSpec:
    name: str
    label: str
    kind: FieldKind
    role: FieldRole
    group: str
    span_class: str | None = None
    required: bool = True
    options: tuple[str, ...] | None = None
    help_text: str | None = None


@dataclass(frozen=True)
class DocumentSpec:
    id: str
    name: str
    description: str
    template_files: tuple[str, ...]
    fields: tuple[FieldSpec, ...]
