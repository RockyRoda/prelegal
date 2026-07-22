"use client";

import { useState, type FormEvent } from "react";
import { sendDocumentChatMessage } from "@/lib/documents/api";
import type { ChatMessage } from "@/lib/documents/types";

const initialMessages: ChatMessage[] = [
  {
    role: "assistant",
    content: "Hi! What kind of legal document do you need today?",
  },
];

export default function DocumentChatPanel({
  docId,
  fieldValues,
  onUpdate,
}: {
  docId: string | null;
  fieldValues: Record<string, string>;
  onUpdate: (docId: string | null, fieldValues: Record<string, string>, html: string) => void;
}) {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!input.trim() || isSending) return;

    const nextMessages: ChatMessage[] = [...messages, { role: "user", content: input }];
    setMessages(nextMessages);
    setInput("");
    setError(null);
    setIsSending(true);

    try {
      const result = await sendDocumentChatMessage(nextMessages, docId, fieldValues);
      setMessages([...nextMessages, { role: "assistant", content: result.reply }]);
      onUpdate(result.docId, result.fieldValues, result.html);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="flex flex-col space-y-4">
      <div className="max-h-[60vh] space-y-3 overflow-y-auto rounded-md border border-zinc-200 p-4 dark:border-zinc-800">
        {messages.map((message, index) => (
          <p
            key={index}
            className={
              message.role === "user"
                ? "text-right text-[#032147] dark:text-zinc-100"
                : "text-zinc-700 dark:text-zinc-300"
            }
          >
            {message.content}
          </p>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          className="flex-1 rounded-md border border-zinc-300 px-3 py-2 text-sm focus:border-[#209dd7] focus:outline-none dark:border-zinc-700 dark:bg-zinc-900"
          placeholder="Type your answer…"
        />
        <button
          type="submit"
          disabled={isSending}
          className="rounded-md bg-[#753991] px-4 py-2 text-sm font-medium text-white hover:bg-[#5f2e75] disabled:opacity-50"
        >
          {isSending ? "Sending…" : "Send"}
        </button>
      </form>
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  );
}
