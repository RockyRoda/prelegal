import { ResolvedTerms } from "./resolve";

/**
 * Transcribed from templates/Mutual-NDA.md (Common Paper Mutual NDA Standard
 * Terms v1.0, CC BY 4.0). The <span class="nda-term"> placeholders correspond
 * to the source template's <span class="coverpage_link"> Cover Page references.
 */
export function buildStandardTermsParagraphs(resolved: ResolvedTerms): string[] {
  const term = (value: string) => `<span class="nda-term">${value}</span>`;

  return [
    `<strong>Introduction</strong>. This Mutual Non-Disclosure Agreement (which incorporates these Standard Terms and the Cover Page (defined below)) (&ldquo;<strong>MNDA</strong>&rdquo;) allows each party (&ldquo;<strong>Disclosing Party</strong>&rdquo;) to disclose or make available information in connection with the ${term(
      resolved.purpose
    )} which (1) the Disclosing Party identifies to the receiving party (&ldquo;<strong>Receiving Party</strong>&rdquo;) as &ldquo;confidential&rdquo;, &ldquo;proprietary&rdquo;, or the like or (2) should be reasonably understood as confidential or proprietary due to its nature and the circumstances of its disclosure (&ldquo;<strong>Confidential Information</strong>&rdquo;). Each party&rsquo;s Confidential Information also includes the existence and status of the parties&rsquo; discussions and information on the Cover Page. Confidential Information includes technical or business information, product designs or roadmaps, requirements, pricing, security and compliance documentation, technology, inventions and know-how. To use this MNDA, the parties must complete and sign a cover page incorporating these Standard Terms (&ldquo;<strong>Cover Page</strong>&rdquo;). Each party is identified on the Cover Page and capitalized terms have the meanings given herein or on the Cover Page.`,

    `<strong>Use and Protection of Confidential Information</strong>. The Receiving Party shall: (a) use Confidential Information solely for the ${term(
      resolved.purpose
    )}; (b) not disclose Confidential Information to third parties without the Disclosing Party&rsquo;s prior written approval, except that the Receiving Party may disclose Confidential Information to its employees, agents, advisors, contractors and other representatives having a reasonable need to know for the ${term(
      resolved.purpose
    )}, provided these representatives are bound by confidentiality obligations no less protective of the Disclosing Party than the applicable terms in this MNDA and the Receiving Party remains responsible for their compliance with this MNDA; and (c) protect Confidential Information using at least the same protections the Receiving Party uses for its own similar information but no less than a reasonable standard of care.`,

    `<strong>Exceptions</strong>. The Receiving Party&rsquo;s obligations in this MNDA do not apply to information that it can demonstrate: (a) is or becomes publicly available through no fault of the Receiving Party; (b) it rightfully knew or possessed prior to receipt from the Disclosing Party without confidentiality restrictions; (c) it rightfully obtained from a third party without confidentiality restrictions; or (d) it independently developed without using or referencing the Confidential Information.`,

    `<strong>Disclosures Required by Law</strong>. The Receiving Party may disclose Confidential Information to the extent required by law, regulation or regulatory authority, subpoena or court order, provided (to the extent legally permitted) it provides the Disclosing Party reasonable advance notice of the required disclosure and reasonably cooperates, at the Disclosing Party&rsquo;s expense, with the Disclosing Party&rsquo;s efforts to obtain confidential treatment for the Confidential Information.`,

    `<strong>Term and Termination</strong>. This MNDA commences on the ${term(
      resolved.effectiveDate
    )} and expires at the end of the ${term(
      resolved.mndaTerm
    )}. Either party may terminate this MNDA for any or no reason upon written notice to the other party. The Receiving Party&rsquo;s obligations relating to Confidential Information will survive for ${term(
      resolved.termOfConfidentiality
    )}, despite any expiration or termination of this MNDA.`,

    `<strong>Return or Destruction of Confidential Information</strong>. Upon expiration or termination of this MNDA or upon the Disclosing Party&rsquo;s earlier request, the Receiving Party will: (a) cease using Confidential Information; (b) promptly after the Disclosing Party&rsquo;s written request, destroy all Confidential Information in the Receiving Party&rsquo;s possession or control or return it to the Disclosing Party; and (c) if requested by the Disclosing Party, confirm its compliance with these obligations in writing. As an exception to subsection (b), the Receiving Party may retain Confidential Information in accordance with its standard backup or record retention policies or as required by law, but the terms of this MNDA will continue to apply to the retained Confidential Information.`,

    `<strong>Proprietary Rights</strong>. The Disclosing Party retains all of its intellectual property and other rights in its Confidential Information and its disclosure to the Receiving Party grants no license under such rights.`,

    `<strong>Disclaimer</strong>. ALL CONFIDENTIAL INFORMATION IS PROVIDED &ldquo;AS IS&rdquo;, WITH ALL FAULTS, AND WITHOUT WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.`,

    `<strong>Governing Law and Jurisdiction</strong>. This MNDA and all matters relating hereto are governed by, and construed in accordance with, the laws of the State of ${term(
      resolved.governingLaw
    )}, without regard to the conflict of laws provisions of such ${term(
      resolved.governingLaw
    )}. Any legal suit, action, or proceeding relating to this MNDA must be instituted in the federal or state courts located in ${term(
      resolved.jurisdiction
    )}. Each party irrevocably submits to the exclusive jurisdiction of such ${term(
      resolved.jurisdiction
    )} in any such suit, action, or proceeding.`,

    `<strong>Equitable Relief</strong>. A breach of this MNDA may cause irreparable harm for which monetary damages are an insufficient remedy. Upon a breach of this MNDA, the Disclosing Party is entitled to seek appropriate equitable relief, including an injunction, in addition to its other remedies.`,

    `<strong>General</strong>. Neither party has an obligation under this MNDA to disclose Confidential Information to the other or proceed with any proposed transaction. Neither party may assign this MNDA without the prior written consent of the other party, except that either party may assign this MNDA in connection with a merger, reorganization, acquisition or other transfer of all or substantially all its assets or voting securities. Any assignment in violation of this Section is null and void. This MNDA will bind and inure to the benefit of each party&rsquo;s permitted successors and assigns. Waivers must be signed by the waiving party&rsquo;s authorized representative and cannot be implied from conduct. If any provision of this MNDA is held unenforceable, it will be limited to the minimum extent necessary so the rest of this MNDA remains in effect. This MNDA (including the Cover Page) constitutes the entire agreement of the parties with respect to its subject matter, and supersedes all prior and contemporaneous understandings, agreements, representations, and warranties, whether written or oral, regarding such subject matter. This MNDA may only be amended, modified, waived, or supplemented by an agreement in writing signed by both parties. Notices, requests and approvals under this MNDA must be sent in writing to the email or postal addresses on the Cover Page and are deemed delivered on receipt. This MNDA may be executed in counterparts, including electronic copies, each of which is deemed an original and which together form the same agreement.`,
  ];
}
