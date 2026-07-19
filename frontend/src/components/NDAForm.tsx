"use client";

import { NDAFormData, PartyDetails, TermChoice } from "@/lib/nda/types";

const inputClasses =
  "mt-1 block w-full rounded-md border border-zinc-300 px-3 py-2 text-sm shadow-sm focus:border-zinc-500 focus:outline-none dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100";

function Field({
  label,
  value,
  onChange,
  required,
  textarea,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
  textarea?: boolean;
  type?: string;
}) {
  return (
    <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300">
      {label}
      {required && <span className="text-red-600"> *</span>}
      {textarea ? (
        <textarea
          value={value}
          required={required}
          onChange={(event) => onChange(event.target.value)}
          rows={2}
          className={inputClasses}
        />
      ) : (
        <input
          type={type}
          value={value}
          required={required}
          onChange={(event) => onChange(event.target.value)}
          className={inputClasses}
        />
      )}
    </label>
  );
}

function TermFieldset({
  legend,
  term,
  onChange,
}: {
  legend: string;
  term: TermChoice;
  onChange: (term: TermChoice) => void;
}) {
  return (
    <fieldset className="space-y-2">
      <legend className="text-sm font-medium text-zinc-900 dark:text-zinc-100">{legend}</legend>
      <label className="flex items-center gap-2 text-sm text-zinc-700 dark:text-zinc-300">
        <input
          type="radio"
          checked={term.type === "expires"}
          onChange={() => onChange({ ...term, type: "expires" })}
        />
        Expires after
        <input
          type="number"
          min={1}
          value={term.years}
          disabled={term.type !== "expires"}
          onChange={(event) => onChange({ ...term, years: Number(event.target.value) || 1 })}
          className="w-16 rounded border border-zinc-300 px-2 py-1 text-sm disabled:opacity-50 dark:border-zinc-700 dark:bg-zinc-900"
        />
        year(s)
      </label>
      <label className="flex items-center gap-2 text-sm text-zinc-700 dark:text-zinc-300">
        <input
          type="radio"
          checked={term.type === "perpetual"}
          onChange={() => onChange({ ...term, type: "perpetual" })}
        />
        No fixed expiration
      </label>
    </fieldset>
  );
}

function PartyFieldset({
  legend,
  party,
  onChange,
}: {
  legend: string;
  party: PartyDetails;
  onChange: (party: PartyDetails) => void;
}) {
  function update<K extends keyof PartyDetails>(key: K, value: PartyDetails[K]) {
    onChange({ ...party, [key]: value });
  }

  return (
    <fieldset className="space-y-3 rounded-md border border-zinc-200 p-4 dark:border-zinc-800">
      <legend className="px-1 text-sm font-medium text-zinc-900 dark:text-zinc-100">
        {legend}
      </legend>
      <Field label="Name" required value={party.name} onChange={(v) => update("name", v)} />
      <Field label="Title" value={party.title} onChange={(v) => update("title", v)} />
      <Field
        label="Company"
        required
        value={party.company}
        onChange={(v) => update("company", v)}
      />
      <Field
        label="Notice Address"
        value={party.noticeAddress}
        onChange={(v) => update("noticeAddress", v)}
        textarea
      />
    </fieldset>
  );
}

export default function NDAForm({
  data,
  onChange,
}: {
  data: NDAFormData;
  onChange: (data: NDAFormData) => void;
}) {
  function set<K extends keyof NDAFormData>(key: K, value: NDAFormData[K]) {
    onChange({ ...data, [key]: value });
  }

  return (
    <div className="space-y-6">
      <Field
        label="Purpose"
        required
        value={data.purpose}
        onChange={(v) => set("purpose", v)}
        textarea
      />

      <Field
        label="Effective Date"
        required
        type="date"
        value={data.effectiveDate}
        onChange={(v) => set("effectiveDate", v)}
      />

      <TermFieldset
        legend="MNDA Term"
        term={data.mndaTerm}
        onChange={(term) => set("mndaTerm", term)}
      />

      <TermFieldset
        legend="Term of Confidentiality"
        term={data.termOfConfidentiality}
        onChange={(term) => set("termOfConfidentiality", term)}
      />

      <Field
        label="Governing Law (State)"
        required
        value={data.governingLaw}
        onChange={(v) => set("governingLaw", v)}
      />

      <Field
        label="Jurisdiction (courts located in)"
        required
        value={data.jurisdiction}
        onChange={(v) => set("jurisdiction", v)}
      />

      <Field
        label="MNDA Modifications (optional)"
        value={data.modifications}
        onChange={(v) => set("modifications", v)}
        textarea
      />

      <PartyFieldset legend="Party 1" party={data.party1} onChange={(p) => set("party1", p)} />
      <PartyFieldset legend="Party 2" party={data.party2} onChange={(p) => set("party2", p)} />
    </div>
  );
}
