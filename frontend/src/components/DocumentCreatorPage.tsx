"use client";

import { useEffect, useState } from "react";
import DocumentChatPanel from "@/components/DocumentChatPanel";
import DocumentPreview from "@/components/DocumentPreview";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import { fetchDocumentDetail, fetchDocumentHistory } from "@/lib/documents/api";
import type { DocumentHistoryItem } from "@/lib/documents/types";
import type { AuthSession } from "@/lib/auth/types";

interface DocumentCreatorPageProps {
  session: AuthSession;
  onSignOut: () => void;
}

export default function DocumentCreatorPage({ session, onSignOut }: DocumentCreatorPageProps) {
  const [docId, setDocId] = useState<string | null>(null);
  const [documentId, setDocumentId] = useState<number | null>(null);
  const [fieldValues, setFieldValues] = useState<Record<string, string>>({});
  const [previewHtml, setPreviewHtml] = useState("");
  const [welcomeMessage, setWelcomeMessage] = useState<string | undefined>(undefined);
  const [history, setHistory] = useState<DocumentHistoryItem[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [chatKey, setChatKey] = useState(0);

  const { user, token } = session;

  useEffect(() => {
    refreshHistory();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function refreshHistory() {
    try {
      const { documents } = await fetchDocumentHistory(token);
      setHistory(documents);
    } catch {
      // History is a convenience list; a failed load shouldn't block document creation.
    }
  }

  function handleUpdate(
    nextDocId: string | null,
    nextDocumentId: number | null,
    nextFieldValues: Record<string, string>,
    html: string
  ) {
    setDocId(nextDocId);
    setDocumentId(nextDocumentId);
    setFieldValues(nextFieldValues);
    setPreviewHtml(html);
    if (nextDocumentId !== null) {
      refreshHistory();
    }
  }

  function handleStartOver() {
    setDocId(null);
    setDocumentId(null);
    setFieldValues({});
    setPreviewHtml("");
    setWelcomeMessage(undefined);
    setError(null);
    setChatKey((key) => key + 1);
  }

  async function handleResume(item: DocumentHistoryItem) {
    setError(null);
    try {
      const detail = await fetchDocumentDetail(item.documentId, token);
      setDocId(detail.docId);
      setDocumentId(detail.documentId);
      setFieldValues(detail.fieldValues);
      setPreviewHtml(detail.html);
      setWelcomeMessage(`Welcome back! Continuing your ${item.docName}. Let's pick up where you left off.`);
      setChatKey((key) => key + 1);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load that document.");
    }
  }

  async function handleDownload() {
    if (!docId) return;
    setError(null);
    setIsGenerating(true);

    try {
      const response = await fetch("/api/generate-pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ docId, fieldValues }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate the PDF. Please try again.");
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${docId}.pdf`;
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
    <div className="flex min-h-screen flex-col bg-zinc-50 dark:bg-zinc-950">
      <header className="border-b border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
        <div className="mx-auto flex max-w-7xl items-start justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-semibold text-brand-navy dark:text-zinc-50">
              Prelegal Document Creator
            </h1>
            <p className="mt-1 text-sm text-brand-gray">
              Chat with the assistant to pick a document and fill in its details, then download it as a PDF.
            </p>
          </div>
          <div className="flex shrink-0 items-center gap-3 pt-1 text-sm">
            <span className="text-brand-gray">{user.name}</span>
            <button type="button" onClick={onSignOut} className="text-brand-blue hover:underline">
              Sign out
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto grid w-full max-w-7xl flex-1 grid-cols-1 gap-8 px-6 py-8 lg:grid-cols-2">
        <div className="space-y-6">
          {history.length > 0 && (
            <Card className="p-4">
              <h2 className="text-sm font-semibold text-brand-navy dark:text-zinc-50">Your documents</h2>
              <ul className="mt-2 space-y-1">
                {history.map((item) => (
                  <li key={item.documentId}>
                    <button
                      type="button"
                      onClick={() => handleResume(item)}
                      disabled={item.documentId === documentId}
                      className="w-full rounded-md px-2 py-1.5 text-left text-sm text-zinc-700 hover:bg-zinc-100 disabled:cursor-default disabled:bg-zinc-100 disabled:font-medium dark:text-zinc-300 dark:hover:bg-zinc-800 dark:disabled:bg-zinc-800"
                    >
                      {item.docName}
                      <span className="ml-2 text-xs text-brand-gray">
                        {new Date(item.updatedAt).toLocaleString()}
                      </span>
                    </button>
                  </li>
                ))}
              </ul>
            </Card>
          )}

          <DocumentChatPanel
            key={chatKey}
            docId={docId}
            documentId={documentId}
            fieldValues={fieldValues}
            token={token}
            welcomeMessage={welcomeMessage}
            onUpdate={handleUpdate}
          />

          <div className="flex items-center gap-4">
            <Button variant="secondary" onClick={handleDownload} disabled={!docId || isGenerating}>
              {isGenerating ? "Generating…" : "Download PDF"}
            </Button>
            {docId && (
              <button type="button" onClick={handleStartOver} className="text-sm text-brand-blue hover:underline">
                Start over with a different document
              </button>
            )}
            {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}
          </div>
        </div>

        <div className="lg:sticky lg:top-8 lg:self-start">
          <Card className="max-h-[85vh] overflow-y-auto p-8">
            <DocumentPreview html={previewHtml} />
          </Card>
        </div>
      </div>

      <footer className="border-t border-zinc-200 bg-white px-6 py-4 dark:border-zinc-800 dark:bg-zinc-900">
        <p className="mx-auto max-w-7xl text-xs text-brand-gray">
          Documents generated by Prelegal are AI-assisted drafts, not legal advice. Have them reviewed by a
          licensed attorney before you rely on or sign them.
        </p>
      </footer>
    </div>
  );
}
