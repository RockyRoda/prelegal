import { NDAFormData, PartyDetails } from "./types";

function emptyParty(): PartyDetails {
  return { name: "", title: "", company: "", noticeAddress: "" };
}

export function defaultNDAFormData(): NDAFormData {
  return {
    purpose: "Evaluating whether to enter into a business relationship with the other party.",
    effectiveDate: new Date().toISOString().slice(0, 10),
    mndaTerm: { type: "expires", years: 1 },
    termOfConfidentiality: { type: "expires", years: 1 },
    governingLaw: "",
    jurisdiction: "",
    modifications: "",
    party1: emptyParty(),
    party2: emptyParty(),
  };
}
