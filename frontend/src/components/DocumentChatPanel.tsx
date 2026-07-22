"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import { sendDocumentChatMessage } from "@/lib/documents/api";
import type { ChatMessage } from "@/lib/documents/types";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";

const DEFAULT_WELCOME = "Hi! What kind of legal document do you need today?";

export default function DocumentChatPanel({
  docId,
  documentId,
  fieldValues,
  token,
  welcomeMessage,
  onUpdate,
}: {
  docId: string | null;
  documentId: number | null;
  fieldValues: Record<string, string>;
  token: string;
  welcomeMessage?: string;
  onUpdate: (docId: string | null, documentId: number | null, fieldValues: Record<string, string>, html: string) => void;
}) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: "assistant", content: welcomeMessage ?? DEFAULT_WELCOME },
  ]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!input.trim() || isSending) return;

    const nextMessages: ChatMessage[] = [...messages, { role: "user", content: input }];
    setMessages(nextMessages);
    setInput("");
    setError(null);
    setIsSending(true);

    try {
      const result = await sendDocumentChatMessage(nextMessages, docId, documentId, fieldValues, token);
      setMessages([...nextMessages, { role: "assistant", content: result.reply }]);
      onUpdate(result.docId, result.documentId, result.fieldValues, result.html);
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
                ? "text-right text-brand-navy dark:text-zinc-100"
                : "text-zinc-700 dark:text-zinc-300"
            }
          >
            {message.content}
          </p>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <Input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Type your answer…"
        />
        <Button type="submit" disabled={isSending}>
          {isSending ? "Sending…" : "Send"}
        </Button>
      </form>
      {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}
    </div>
  );
}
