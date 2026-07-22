"""Field registry for every document in the root catalog.json.

Each document's fields were reverse-engineered from its Standard Terms body
(most of these documents ship only that body - the actual Key Terms/Cover
Page/SOW/Order Form template referenced by their placeholder spans isn't in
this repo). Classification rule, applied consistently across all documents:

- DEFINED_TERM: only the party-role names (Customer, Provider, Company,
  Partner, ...). These stay as literal text in the body; the real value is
  only shown once, on a generated summary table.
- SUBSTITUTED: everything else with a plausible matching span (dates,
  durations, amounts, governing law, ...). The span text is replaced with the
  real value everywhere it appears in the body.
- SUMMARY_ONLY: fields with no span in the body at all (e.g. notice
  addresses, signature block details) - shown only on the summary table.

Every field, regardless of role, always appears on the generated summary
table - inline body substitution is a best-effort enhancement on top of that,
not the source of truth, since exact span wording can't be verified without
the real Key Terms templates.
"""

from .schema import DocumentSpec, FieldKind, FieldRole, FieldSpec

_STRING = FieldKind.STRING
_DATE = FieldKind.DATE
_ENUM = FieldKind.ENUM
_TERM = FieldRole.DEFINED_TERM
_SUB = FieldRole.SUBSTITUTED
_SUMMARY = FieldRole.SUMMARY_ONLY

MNDA = DocumentSpec(
    id="mnda",
    name="Mutual Non-Disclosure Agreement (MNDA)",
    description="A mutual non-disclosure agreement that allows two parties to disclose confidential information to each other in connection with evaluating a potential business relationship.",
    template_files=("Mutual-NDA-coverpage.md", "Mutual-NDA.md"),
    fields=(
        FieldSpec("purpose", "Purpose", _STRING, _SUB, "Cover Page", "coverpage_link"),
        FieldSpec("effectiveDate", "Effective Date", _DATE, _SUB, "Cover Page", "coverpage_link"),
        FieldSpec(
            "mndaTerm", "MNDA Term", _STRING, _SUB, "Cover Page", "coverpage_link",
            help_text="e.g. 'expires 1 year(s) from the Effective Date' or 'continues until terminated in accordance with the terms of the MNDA'",
        ),
        FieldSpec(
            "termOfConfidentiality", "Term of Confidentiality", _STRING, _SUB, "Cover Page", "coverpage_link",
            help_text="e.g. '1 year(s) from Effective Date' or 'in perpetuity'",
        ),
        FieldSpec("governingLaw", "Governing Law", _STRING, _SUB, "Cover Page", "coverpage_link"),
        FieldSpec("jurisdiction", "Jurisdiction", _STRING, _SUB, "Cover Page", "coverpage_link"),
        FieldSpec("modifications", "MNDA Modifications", _STRING, _SUMMARY, "Cover Page", required=False),
        FieldSpec("party1Name", "Party 1 Name", _STRING, _SUMMARY, "Parties"),
        FieldSpec("party1Title", "Party 1 Title", _STRING, _SUMMARY, "Parties", required=False),
        FieldSpec("party1Company", "Party 1 Company", _STRING, _SUMMARY, "Parties"),
        FieldSpec("party1NoticeAddress", "Party 1 Notice Address", _STRING, _SUMMARY, "Parties", required=False),
        FieldSpec("party2Name", "Party 2 Name", _STRING, _SUMMARY, "Parties"),
        FieldSpec("party2Title", "Party 2 Title", _STRING, _SUMMARY, "Parties", required=False),
        FieldSpec("party2Company", "Party 2 Company", _STRING, _SUMMARY, "Parties"),
        FieldSpec("party2NoticeAddress", "Party 2 Notice Address", _STRING, _SUMMARY, "Parties", required=False),
    ),
)

CSA = DocumentSpec(
    id="csa",
    name="Cloud Service Agreement (CSA)",
    description="A standard agreement for selling and buying cloud software and SaaS products, covering access and use of the service, payment, term, warranties, liability, indemnification, and confidentiality.",
    template_files=("CSA.md",),
    fields=(
        FieldSpec("customerLegalName", "Customer", _STRING, _TERM, "Parties", "coverpage_link"),
        FieldSpec("providerLegalName", "Provider", _STRING, _TERM, "Parties", "coverpage_link"),
        FieldSpec("effectiveDate", "Effective Date", _DATE, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("governingLaw", "Governing Law", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("chosenCourts", "Chosen Courts", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("generalCapAmount", "General Cap Amount", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("increasedClaims", "Increased Claims", _STRING, _SUB, "Key Terms", "keyterms_link", required=False, help_text="claim categories subject to the higher cap, comma-separated, or leave blank"),
        FieldSpec("increasedCapAmount", "Increased Cap Amount", _STRING, _SUB, "Key Terms", "keyterms_link", required=False),
        FieldSpec("unlimitedClaims", "Unlimited Claims", _STRING, _SUB, "Key Terms", "keyterms_link", required=False, help_text="claim categories excluded from any cap, comma-separated, or leave blank"),
        FieldSpec("providerCoveredClaims", "Provider Covered Claims", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("customerCoveredClaims", "Customer Covered Claims", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("additionalWarranties", "Additional Warranties", _STRING, _SUB, "Key Terms", "keyterms_link", required=False),
        FieldSpec("orderDate", "Order Date", _DATE, _SUB, "Order Form", "orderform_link"),
        FieldSpec("subscriptionPeriod", "Subscription Period", _STRING, _SUB, "Order Form", "orderform_link"),
        FieldSpec("technicalSupport", "Technical Support", _STRING, _SUB, "Order Form", "orderform_link"),
        FieldSpec("useLimitations", "Use Limitations", _STRING, _SUB, "Order Form", "orderform_link", required=False),
        FieldSpec("paymentMethod", "Payment Method", _ENUM, _SUB, "Order Form", "orderform_link", options=("Invoicing", "Automatic Payment")),
        FieldSpec("paymentProcess", "Payment Process", _STRING, _SUB, "Order Form", "orderform_link"),
    ),
)

DESIGN_PARTNER = DocumentSpec(
    id="design-partner",
    name="Design Partner Agreement",
    description="An agreement granting an early customer or partner access to a product in exchange for feedback to help develop and improve the product before general availability.",
    template_files=("design-partner-agreement.md",),
    fields=(
        FieldSpec("providerName", "Provider", _STRING, _TERM, "Parties", "keyterms_link"),
        FieldSpec("partnerName", "Design Partner", _STRING, _TERM, "Parties", "keyterms_link"),
        FieldSpec("programName", "Program Name", _STRING, _SUB, "Program", "keyterms_link"),
        FieldSpec("effectiveDate", "Effective Date", _DATE, _SUB, "Program", "keyterms_link"),
        FieldSpec("termLength", "Term", _STRING, _SUB, "Program", "keyterms_link", help_text="e.g. '12 months'"),
        FieldSpec("fees", "Fees", _STRING, _SUB, "Fees", "keyterms_link", required=False, help_text="dollar amount, or 'none' if the program is free"),
        FieldSpec("governingLaw", "Governing Law", _STRING, _SUB, "Governing Law & Notices", "keyterms_link"),
        FieldSpec("chosenCourts", "Chosen Courts", _STRING, _SUB, "Governing Law & Notices", "keyterms_link"),
        FieldSpec("providerNoticeAddress", "Provider Notice Address", _STRING, _SUMMARY, "Governing Law & Notices", required=False),
        FieldSpec("partnerNoticeAddress", "Partner Notice Address", _STRING, _SUMMARY, "Governing Law & Notices", required=False),
    ),
)

SLA = DocumentSpec(
    id="sla",
    name="Service Level Agreement (SLA)",
    description="A supplemental agreement, designed to be used with the Common Paper Cloud Service Agreement, that defines uptime and support response time commitments and the service credits available if those targets are missed.",
    template_files=("sla.md",),
    fields=(
        FieldSpec("customerLegalName", "Customer", _STRING, _TERM, "Parties", "coverpage_link"),
        FieldSpec("providerLegalName", "Provider", _STRING, _TERM, "Parties", "coverpage_link"),
        FieldSpec("subscriptionPeriod", "Subscription Period", _STRING, _SUB, "Order Form", "orderform_link"),
        FieldSpec("targetUptime", "Target Uptime", _STRING, _SUB, "Uptime", "orderform_link", required=False, help_text="e.g. '99.9%', or leave blank if no uptime commitment applies"),
        FieldSpec("scheduledDowntime", "Scheduled Downtime", _STRING, _SUB, "Uptime", "orderform_link", required=False),
        FieldSpec("uptimeCredit", "Uptime Credit", _STRING, _SUB, "Uptime", "orderform_link", required=False, help_text="the service credit schedule if uptime is missed, e.g. tiers of % credit per shortfall range"),
        FieldSpec("targetResponseTime", "Target Response Time", _STRING, _SUB, "Response Time", "orderform_link", required=False, help_text="e.g. '4 business hours', or leave blank if no response time commitment applies"),
        FieldSpec("supportChannel", "Support Channel", _STRING, _SUB, "Response Time", "orderform_link", required=False),
        FieldSpec("responseTimeCredit", "Response Time Credit", _STRING, _SUB, "Response Time", "orderform_link", required=False),
    ),
)

PSA = DocumentSpec(
    id="psa",
    name="Professional Services Agreement (PSA)",
    description="An agreement for procuring professional services under one or more statements of work, covering deliverables, intellectual property, payment, warranties, liability, and confidentiality.",
    template_files=("psa.md",),
    fields=(
        FieldSpec("customerName", "Customer", _STRING, _TERM, "Parties", "keyterms_link"),
        FieldSpec("providerName", "Provider", _STRING, _TERM, "Parties", "keyterms_link"),
        FieldSpec("effectiveDate", "Effective Date", _DATE, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("governingLaw", "Governing Law", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("chosenCourts", "Chosen Courts", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("generalCapAmount", "General Cap Amount", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("increasedCapAmount", "Increased Cap Amount", _STRING, _SUB, "Key Terms", "keyterms_link", required=False),
        FieldSpec("increasedClaims", "Increased Claims", _STRING, _SUB, "Key Terms", "keyterms_link", required=False, help_text="comma-separated"),
        FieldSpec("unlimitedClaims", "Unlimited Claims", _STRING, _SUB, "Key Terms", "keyterms_link", required=False, help_text="comma-separated"),
        FieldSpec("providerCoveredClaims", "Provider Covered Claims", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("customerCoveredClaims", "Customer Covered Claims", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("insuranceMinimums", "Insurance Minimums", _STRING, _SUB, "Key Terms", "keyterms_link", required=False),
        FieldSpec("additionalWarranties", "Additional Warranties", _STRING, _SUB, "Key Terms", "keyterms_link", required=False),
        FieldSpec("deliverables", "Deliverables", _STRING, _SUB, "SOW", "sow_link", required=False),
        FieldSpec("fees", "Fees", _STRING, _SUB, "SOW", "sow_link"),
        FieldSpec("paymentPeriod", "Payment Period", _STRING, _SUB, "SOW", "sow_link", help_text="e.g. '30 days'"),
        FieldSpec("timeOfAssignment", "Time of Assignment", _ENUM, _SUB, "SOW", "sow_link", options=("Upon Full Payment", "Upon Delivery", "Upon Acceptance")),
        FieldSpec("rejectionPeriod", "Rejection Period", _STRING, _SUB, "SOW", "sow_link", required=False, help_text="e.g. '10 days'"),
        FieldSpec("customerObligations", "Customer Obligations", _STRING, _SUB, "SOW", "sow_link", required=False),
    ),
)

DPA = DocumentSpec(
    id="dpa",
    name="Data Processing Agreement (DPA)",
    description="An agreement governing how a service provider processes personal data on behalf of a customer, including international data transfer mechanisms, subprocessors, security incident response, and audit rights.",
    template_files=("DPA.md",),
    fields=(
        FieldSpec("customerName", "Customer", _STRING, _TERM, "Parties", "keyterms_link"),
        FieldSpec("providerName", "Provider", _STRING, _TERM, "Parties", "keyterms_link"),
        FieldSpec("underlyingAgreement", "Underlying Agreement", _STRING, _SUMMARY, "Parties", required=False, help_text="the primary contract this DPA supplements, e.g. 'the CSA dated ...'"),
        FieldSpec("categoriesOfDataSubjects", "Categories of Data Subjects", _STRING, _SUB, "Processing Details", "keyterms_link", help_text="comma-separated, e.g. 'Employees, End users'"),
        FieldSpec("categoriesOfPersonalData", "Categories of Personal Data", _STRING, _SUB, "Processing Details", "keyterms_link", help_text="comma-separated, e.g. 'Name, Email, IP address'"),
        FieldSpec("specialCategoryData", "Special Category Data", _STRING, _SUB, "Processing Details", "keyterms_link", required=False, help_text="sensitive data categories if any, or 'None'"),
        FieldSpec("natureAndPurposeOfProcessing", "Nature and Purpose of Processing", _STRING, _SUB, "Processing Details", "keyterms_link"),
        FieldSpec("durationOfProcessing", "Duration of Processing", _STRING, _SUB, "Processing Details", "keyterms_link", help_text="e.g. 'Term of the Agreement'"),
        FieldSpec("approvedSubprocessors", "Approved Subprocessors", _STRING, _SUB, "Subprocessors", "keyterms_link", required=False, help_text="comma-separated list of subprocessor name (location, purpose), or 'None'"),
        FieldSpec("governingMemberState", "Governing Member State", _STRING, _SUB, "International Transfers", "keyterms_link", required=False, help_text="only required if EEA standard contractual clauses apply"),
        FieldSpec("securityPolicy", "Security Policy", _STRING, _SUB, "Audit & Security", "keyterms_link"),
        FieldSpec("providerSecurityContact", "Provider Security Contact", _STRING, _SUB, "Audit & Security", "keyterms_link"),
    ),
)

SOFTWARE_LICENSE = DocumentSpec(
    id="software-license",
    name="Software License Agreement",
    description="An agreement licensing on-premises or installed software to a customer, covering license grants, restrictions, updates, warranties, liability, and confidentiality.",
    template_files=("Software-License-Agreement.md",),
    fields=(
        FieldSpec("providerLegalName", "Provider", _STRING, _TERM, "Parties", "coverpage_link"),
        FieldSpec("customerLegalName", "Customer", _STRING, _TERM, "Parties", "coverpage_link"),
        FieldSpec("providerNoticeAddress", "Provider Notice Address", _STRING, _SUMMARY, "Parties", required=False),
        FieldSpec("customerNoticeAddress", "Customer Notice Address", _STRING, _SUMMARY, "Parties", required=False),
        FieldSpec("effectiveDate", "Effective Date", _DATE, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("governingLaw", "Governing Law", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("chosenCourts", "Chosen Courts", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("additionalWarranties", "Additional Warranties", _STRING, _SUB, "Key Terms", "keyterms_link", required=False),
        FieldSpec("generalCapAmount", "General Cap Amount", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("increasedCapAmount", "Increased Cap Amount", _STRING, _SUB, "Key Terms", "keyterms_link", required=False),
        FieldSpec("increasedClaims", "Increased Claims", _STRING, _SUB, "Key Terms", "keyterms_link", required=False, help_text="comma-separated"),
        FieldSpec("unlimitedClaims", "Unlimited Claims", _STRING, _SUB, "Key Terms", "keyterms_link", required=False, help_text="comma-separated"),
        FieldSpec("providerCoveredClaims", "Provider Covered Claims", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("customerCoveredClaims", "Customer Covered Claims", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("orderDate", "Order Date", _DATE, _SUB, "Order Form", "orderform_link"),
        FieldSpec("subscriptionPeriod", "Subscription Period", _STRING, _SUB, "Order Form", "orderform_link"),
        FieldSpec("permittedUses", "Permitted Uses", _STRING, _SUB, "Order Form", "orderform_link"),
        FieldSpec("licenseLimits", "License Limits", _STRING, _SUB, "Order Form", "orderform_link", required=False),
        FieldSpec("paymentProcess", "Payment Process", _ENUM, _SUB, "Order Form", "orderform_link", options=("Invoicing", "Automatic Payment")),
        FieldSpec("warrantyPeriod", "Warranty Period", _STRING, _SUB, "Order Form", "orderform_link", help_text="e.g. '90 days'"),
    ),
)

PARTNERSHIP = DocumentSpec(
    id="partnership",
    name="Partnership Agreement",
    description="An agreement for business partnerships involving mutual obligations, trademark licensing, and fees, covering brand element usage, payment, warranties, liability, and confidentiality.",
    template_files=("Partnership-Agreement.md",),
    fields=(
        FieldSpec("companyName", "Company", _STRING, _TERM, "Parties", "keyterms_link"),
        FieldSpec("partnerName", "Partner", _STRING, _TERM, "Parties", "keyterms_link"),
        FieldSpec("effectiveDate", "Effective Date", _DATE, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("governingLaw", "Governing Law", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("chosenCourts", "Chosen Courts", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("brandGuidelines", "Brand Guidelines", _STRING, _SUB, "Key Terms", "keyterms_link", required=False),
        FieldSpec("additionalWarranties", "Additional Warranties", _STRING, _SUB, "Key Terms", "keyterms_link", required=False),
        FieldSpec("generalCapAmount", "General Cap Amount", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("increasedCapAmount", "Increased Cap Amount", _STRING, _SUB, "Key Terms", "keyterms_link", required=False),
        FieldSpec("increasedClaims", "Increased Claims", _STRING, _SUB, "Key Terms", "keyterms_link", required=False, help_text="comma-separated"),
        FieldSpec("unlimitedClaims", "Unlimited Claims", _STRING, _SUB, "Key Terms", "keyterms_link", required=False, help_text="comma-separated"),
        FieldSpec("companyCoveredClaim", "Company Covered Claim", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("partnerCoveredClaims", "Partner Covered Claims", _STRING, _SUB, "Key Terms", "keyterms_link"),
        FieldSpec("companyObligations", "Company's Obligations", _STRING, _SUB, "Business Terms", "businessterms_link"),
        FieldSpec("partnerObligations", "Partner's Obligations", _STRING, _SUB, "Business Terms", "businessterms_link"),
        FieldSpec("territory", "Territory", _STRING, _SUB, "Business Terms", "businessterms_link", help_text="e.g. 'Worldwide' or a list of countries"),
        FieldSpec("endDate", "End Date", _DATE, _SUB, "Business Terms", "businessterms_link"),
        FieldSpec("paymentProcess", "Payment Process", _STRING, _SUB, "Business Terms", "businessterms_link", required=False),
        FieldSpec("paymentSchedule", "Payment Schedule", _STRING, _SUB, "Business Terms", "businessterms_link", required=False),
    ),
)

PILOT = DocumentSpec(
    id="pilot",
    name="Pilot Agreement",
    description="A short-term trial or evaluation agreement that allows a prospective customer to test a product before committing to a longer-term deal.",
    template_files=("Pilot-Agreement.md",),
    fields=(
        FieldSpec("providerName", "Provider", _STRING, _TERM, "Parties", "orderform_link"),
        FieldSpec("customerName", "Customer", _STRING, _TERM, "Parties", "orderform_link"),
        FieldSpec("providerNoticeAddress", "Provider Notice Address", _STRING, _SUMMARY, "Parties", required=False),
        FieldSpec("customerNoticeAddress", "Customer Notice Address", _STRING, _SUMMARY, "Parties", required=False),
        FieldSpec("effectiveDate", "Effective Date", _DATE, _SUB, "Pilot Terms", "orderform_link"),
        FieldSpec("pilotPeriod", "Pilot Period", _STRING, _SUB, "Pilot Terms", "orderform_link", help_text="e.g. '60 days'"),
        FieldSpec("fees", "Fees", _STRING, _SUB, "Pilot Terms", "orderform_link", required=False, help_text="dollar amount, or 'none' if the pilot is free"),
        FieldSpec("generalCapAmount", "General Cap Amount", _STRING, _SUB, "Liability", "orderform_link"),
        FieldSpec("governingLaw", "Governing Law", _STRING, _SUB, "Governing Law", "orderform_link"),
        FieldSpec("chosenCourts", "Chosen Courts", _STRING, _SUB, "Governing Law", "orderform_link"),
    ),
)

BAA = DocumentSpec(
    id="baa",
    name="Business Associate Agreement (BAA)",
    description="A HIPAA-required agreement between a covered entity and a business associate that governs the use, disclosure, and safeguarding of protected health information (PHI).",
    template_files=("BAA.md",),
    fields=(
        FieldSpec("providerName", "Provider", _STRING, _TERM, "Parties", "keyterms_link"),
        FieldSpec("companyName", "Company", _STRING, _TERM, "Parties", "keyterms_link"),
        FieldSpec("baaEffectiveDate", "BAA Effective Date", _DATE, _SUB, "Term", "keyterms_link"),
        FieldSpec("underlyingAgreement", "Underlying Agreement", _STRING, _SUB, "Term", "keyterms_link", help_text="the primary contract this BAA supplements"),
        FieldSpec("breachNotificationPeriod", "Breach Notification Period", _STRING, _SUB, "Breach Notification", "keyterms_link", help_text="e.g. '5 business days'"),
        FieldSpec("limitations", "Limitations", _STRING, _SUB, "Data Rights & Restrictions", "keyterms_link", required=False, help_text="restrictions on Provider's permitted uses of PHI, or 'none'"),
    ),
)

AI_ADDENDUM = DocumentSpec(
    id="ai-addendum",
    name="AI Addendum",
    description="A supplemental addendum governing the use of AI services within a product, covering permitted uses of inputs and outputs, model training restrictions, ownership, and AI-specific disclaimers.",
    template_files=("AI-Addendum.md",),
    fields=(
        FieldSpec("customerLegalName", "Customer", _STRING, _TERM, "Parties", "coverpage_link"),
        FieldSpec("providerLegalName", "Provider", _STRING, _TERM, "Parties", "coverpage_link"),
        FieldSpec("trainingPermitted", "Training Permitted", _ENUM, _SUMMARY, "AI Training & Improvement", options=("Yes", "No")),
        FieldSpec("trainingData", "Training Data", _STRING, _SUB, "AI Training & Improvement", "coverpage_link", required=False, help_text="only if Training Permitted is Yes"),
        FieldSpec("trainingPurposes", "Training Purposes", _STRING, _SUB, "AI Training & Improvement", "coverpage_link", required=False, help_text="only if Training Permitted is Yes"),
        FieldSpec("trainingRestrictions", "Training Restrictions", _STRING, _SUB, "AI Training & Improvement", "coverpage_link", required=False, help_text="only if Training Permitted is Yes"),
        FieldSpec("improvementRestrictions", "Improvement Restrictions", _STRING, _SUB, "AI Training & Improvement", "coverpage_link", required=False),
    ),
)

DOCUMENTS: dict[str, DocumentSpec] = {
    spec.id: spec
    for spec in (
        MNDA,
        CSA,
        DESIGN_PARTNER,
        SLA,
        PSA,
        DPA,
        SOFTWARE_LICENSE,
        PARTNERSHIP,
        PILOT,
        BAA,
        AI_ADDENDUM,
    )
}
