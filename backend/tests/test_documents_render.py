from app.documents.registry import DOCUMENTS
from app.documents.render import render_document_html


def test_all_documents_render_without_error() -> None:
    for spec in DOCUMENTS.values():
        values = {f.name: (f.options[0] if f.options else "Test Value") for f in spec.fields}
        html = render_document_html(spec, values)
        assert "<article" in html


def test_substituted_field_is_replaced_inline() -> None:
    spec = DOCUMENTS["mnda"]
    html = render_document_html(spec, {"purpose": "evaluating a merger"})
    assert "evaluating a merger" in html


def test_defined_term_field_stays_literal_in_body_only_shown_in_summary() -> None:
    spec = DOCUMENTS["csa"]
    html = render_document_html(spec, {"customerLegalName": "Acme Inc"})
    assert html.count("Acme Inc") == 1


def test_date_field_is_formatted() -> None:
    spec = DOCUMENTS["mnda"]
    html = render_document_html(spec, {"effectiveDate": "2026-08-01"})
    assert "August 1, 2026" in html
