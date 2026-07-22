"""Renders a document to HTML: real template markdown + field substitution.

Only the last file in a DocumentSpec's template_files is rendered - for MNDA
that's Mutual-NDA.md, the Standard Terms body. Earlier files (MNDA's
coverpage) exist only as the historical source used to author registry.py's
field list; we don't render them, since the other 10 documents have no
equivalent coverpage file and every document should look structurally the
same. Instead, a summary table is generated from field values for every
field, which is the only place a DEFINED_TERM field's real value is shown.
"""

import html
import re
from datetime import date

import markdown as md

from .schema import DocumentSpec, FieldKind, FieldRole
from .templates import read_template


def _format_date(value: str) -> str:
    try:
        year, month, day = (int(part) for part in value.split("-"))
        parsed = date(year, month, day)
        return f"{parsed:%B} {parsed.day}, {parsed.year}"
    except (ValueError, AttributeError):
        return html.escape(value)


def _format_value(kind: FieldKind, value: str) -> str:
    if not value:
        return "&mdash;"
    if kind == FieldKind.DATE:
        return _format_date(value)
    return html.escape(value)


def _substitute_body(body_html: str, spec: DocumentSpec, values: dict[str, str]) -> str:
    for field in spec.fields:
        if field.role != FieldRole.SUBSTITUTED or not field.span_class:
            continue
        value = values.get(field.name, "")
        if not value:
            continue
        pattern = re.compile(
            rf'<span class="{re.escape(field.span_class)}">{re.escape(field.label)}</span>'
        )
        replacement = f'<span class="doc-term">{_format_value(field.kind, value)}</span>'
        body_html = pattern.sub(replacement, body_html)
    return body_html


def _summary_table_html(spec: DocumentSpec, values: dict[str, str]) -> str:
    rows = []
    current_group = None
    for field in spec.fields:
        if field.group != current_group:
            current_group = field.group
            rows.append(f'<tr class="doc-summary-group"><th colspan="2">{html.escape(current_group)}</th></tr>')
        value = _format_value(field.kind, values.get(field.name, ""))
        rows.append(f"<tr><th>{html.escape(field.label)}</th><td>{value}</td></tr>")
    return f'<table class="doc-summary-table">{"".join(rows)}</table>'


def render_document_html(spec: DocumentSpec, values: dict[str, str]) -> str:
    body_source = read_template(spec.template_files[-1])
    body_html = md.markdown(body_source, extensions=["tables", "sane_lists"])
    body_html = _substitute_body(body_html, spec, values)
    summary_html = _summary_table_html(spec, values)

    return f"""<article class="doc-document">
    <h1 class="doc-title">{html.escape(spec.name)}</h1>
    <section>
      <h2 class="doc-section-heading">Summary</h2>
      {summary_html}
    </section>
    <section>
      {body_html}
    </section>
    </article>"""
