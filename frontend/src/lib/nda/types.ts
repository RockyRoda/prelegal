export type TermOptionType = "expires" | "perpetual";

export interface TermChoice {
  type: TermOptionType;
  /** Number of years until expiry. Only meaningful when type is "expires". */
  years: number;
}

export interface PartyDetails {
  name: string;
  title: string;
  company: string;
  noticeAddress: string;
}

export interface NDAFormData {
  purpose: string;
  effectiveDate: string;
  mndaTerm: TermChoice;
  termOfConfidentiality: TermChoice;
  governingLaw: string;
  jurisdiction: string;
  modifications: string;
  party1: PartyDetails;
  party2: PartyDetails;
}
