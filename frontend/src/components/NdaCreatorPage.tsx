"use client";

import { useState, type FormEvent } from "react";
import NDAForm from "@/components/NDAForm";
import NDADocument from "@/components/NDADocument";
import { defaultNDAFormData } from "@/lib/nda/defaults";
import { NDAFormData } from "@/lib/nda/types";
import type { AuthUser } from "@/lib/auth/types";

interface NdaCreatorPageProps {
  user: AuthUser;
  onSignOut: () => void;
}

export default function NdaCreatorPage({ user, onSignOut }: NdaCreatorPageProps) {
  const [data, setData] = useState<NDAFormData>(defaultNDAFormData);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsGenerating(true);

    try {
      const response = await fetch("/api/generate-pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Failed to generate the PDF. Please try again.");
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "mutual-nda.pdf";
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsGenerating(false);
    }
  }

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950">
      <header className="border-b border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
        <div className="mx-auto flex max-w-7xl items-start justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-semibold text-zinc-900 dark:text-zinc-50">
              Mutual NDA Creator
            </h1>
            <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
              Fill in the details below to generate a Mutual Non-Disclosure Agreement based on the
              Common Paper standard, and download it as a PDF.
            </p>
          </div>
          <div className="flex shrink-0 items-center gap-3 pt-1 text-sm">
            <span className="text-zinc-600 dark:text-zinc-400">{user.name}</span>
            <button
              type="button"
              onClick={onSignOut}
              className="text-[#209dd7] hover:underline"
            >
              Sign out
            </button>
          </div>
        </div>
      </header>

      <form
        onSubmit={handleSubmit}
        className="mx-auto grid max-w-7xl grid-cols-1 gap-8 px-6 py-8 lg:grid-cols-2"
      >
        <div>
          <NDAForm data={data} onChange={setData} />

          <div className="mt-6 flex items-center gap-4">
            <button
              type="submit"
              disabled={isGenerating}
              className="rounded-md bg-zinc-900 px-5 py-2.5 text-sm font-medium text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200"
            >
              {isGenerating ? "Generating…" : "Download PDF"}
            </button>
            {error && <p className="text-sm text-red-600">{error}</p>}
          </div>
        </div>

        <div className="lg:sticky lg:top-8 lg:self-start">
          <div className="max-h-[85vh] overflow-y-auto rounded-lg border border-zinc-200 bg-white p-8 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
            <NDADocument data={data} />
          </div>
        </div>
      </form>
    </div>
  );
}
