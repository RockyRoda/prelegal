import { NDAFormData, PartyDetails, TermChoice, TermOptionType } from "./types";
import { formatDate, resolveTerms } from "./resolve";
import { buildStandardTermsParagraphs } from "./standardTerms";
import { escapeHtml } from "./html";

function choiceListHtml(
  selected: TermOptionType,
  options: { type: TermOptionType; label: string }[]
): string {
  const items = options
    .map(
      (option) =>
        `<li>${selected === option.type ? "☒" : "☐"} ${escapeHtml(option.label)}</li>`
    )
    .join("");
  return `<ul class="nda-choice-list">${items}</ul>`;
}

function mndaTermChoiceListHtml(term: TermChoice): string {
  return choiceListHtml(term.type, [
    { type: "expires", label: `Expires ${term.years} year(s) from Effective Date.` },
    {
      type: "perpetual",
      label: "Continues until terminated in accordance with the terms of the MNDA.",
    },
  ]);
}

function confidentialityChoiceListHtml(term: TermChoice): string {
  return choiceListHtml(term.type, [
    {
      type: "expires",
      label: `${term.years} year(s) from Effective Date, but in the case of trade secrets until Confidential Information is no longer considered a trade secret under applicable laws.`,
    },
    { type: "perpetual", label: "In perpetuity." },
  ]);
}

function fieldHtml(label: string, valueHtml: string): string {
  return `<div class="nda-field"><span class="nda-field-label">${label}</span><span class="nda-field-value">${valueHtml}</span></div>`;
}

function signatureTableHtml(party1: PartyDetails, party2: PartyDetails): string {
  const rows: [string, keyof PartyDetails | null][] = [
    ["Signature", null],
    ["Print Name", "name"],
    ["Title", "title"],
    ["Company", "company"],
    ["Notice Address", "noticeAddress"],
    ["Date", null],
  ];

  const cell = (party: PartyDetails, field: keyof PartyDetails | null) =>
    field ? escapeHtml(party[field] || "—") : "";

  const rowsHtml = rows
    .map(
      ([label, field]) =>
        `<tr><th>${label}</th><td>${cell(party1, field)}</td><td>${cell(party2, field)}</td></tr>`
    )
    .join("");

  return `<table class="nda-signature-table"><thead><tr><th></th><th>Party 1</th><th>Party 2</th></tr></thead><tbody>${rowsHtml}</tbody></table>`;
}

/**
 * Renders the full Mutual NDA (cover page + standard terms) to an HTML
 * string. Used both for the on-screen preview and, server-side, to build the
 * page handed to Puppeteer for the PDF, so the two never drift apart.
 */
export function renderNDADocumentHtml(data: NDAFormData): string {
  const resolved = resolveTerms(data);
  const paragraphsHtml = buildStandardTermsParagraphs(resolved)
    .map((html) => `<li>${html}</li>`)
    .join("");

  const modificationsHtml = data.modifications
    ? fieldHtml("MNDA Modifications", escapeHtml(data.modifications))
    : "";

  return `<article class="nda-document">
    <h1 class="nda-title">Mutual Non-Disclosure Agreement</h1>
    <section>
      <h2 class="nda-section-heading">Cover Page</h2>
      ${fieldHtml("Purpose", escapeHtml(data.purpose || "—"))}
      ${fieldHtml("Effective Date", formatDate(data.effectiveDate))}
      ${fieldHtml("MNDA Term", mndaTermChoiceListHtml(data.mndaTerm))}
      ${fieldHtml("Term of Confidentiality", confidentialityChoiceListHtml(data.termOfConfidentiality))}
      ${fieldHtml(
        "Governing Law &amp; Jurisdiction",
        `Governing Law: ${escapeHtml(data.governingLaw || "—")}<br />Jurisdiction: ${escapeHtml(
          data.jurisdiction || "—"
        )}`
      )}
      ${modificationsHtml}
      ${signatureTableHtml(data.party1, data.party2)}
    </section>
    <section>
      <h2 class="nda-section-heading">Standard Terms</h2>
      <ol class="nda-standard-terms">${paragraphsHtml}</ol>
    </section>
    <p class="nda-footer-note">Based on the Common Paper Mutual Non-Disclosure Agreement Version 1.0, free to use under CC BY 4.0.</p>
  </article>`;
}
