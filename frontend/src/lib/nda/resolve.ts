import { NDAFormData, TermChoice } from "./types";
import { escapeHtml } from "./html";

export function formatDate(isoDate: string): string {
  if (!isoDate) return "[Effective Date]";
  const [year, month, day] = isoDate.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC",
  });
}

export function describeMndaTerm(term: TermChoice): string {
  if (term.type === "perpetual") {
    return "the date this MNDA is terminated by either party in accordance with its terms";
  }
  return `${term.years} year(s) from the Effective Date`;
}

export function describeTermOfConfidentiality(term: TermChoice): string {
  if (term.type === "perpetual") {
    return "in perpetuity";
  }
  return `${term.years} year(s) from the Effective Date, but in the case of trade secrets until the Confidential Information is no longer considered a trade secret under applicable law`;
}

export interface ResolvedTerms {
  purpose: string;
  effectiveDate: string;
  mndaTerm: string;
  termOfConfidentiality: string;
  governingLaw: string;
  jurisdiction: string;
}

/**
 * All values here are derived from user-supplied input and get interpolated
 * directly into HTML strings (see standardTerms.ts and renderDocument.ts),
 * so they must be HTML-escaped here at the source. This includes mndaTerm
 * and termOfConfidentiality: `years` is typed as a number, but the API route
 * accepts raw, unvalidated JSON, so a request built by hand (rather than the
 * form) could still put arbitrary text there.
 */
export function resolveTerms(data: NDAFormData): ResolvedTerms {
  return {
    purpose: escapeHtml(data.purpose || "[Purpose]"),
    effectiveDate: formatDate(data.effectiveDate),
    mndaTerm: escapeHtml(describeMndaTerm(data.mndaTerm)),
    termOfConfidentiality: escapeHtml(describeTermOfConfidentiality(data.termOfConfidentiality)),
    governingLaw: escapeHtml(data.governingLaw || "[Governing Law]"),
    jurisdiction: escapeHtml(data.jurisdiction || "[Jurisdiction]"),
  };
}
