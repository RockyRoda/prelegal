"use client";

import { useState, type FormEvent } from "react";
import type { NDAFormData } from "@/lib/nda/types";
import { sendNDAChatMessage, type ChatMessage } from "@/lib/nda/chatApi";

const initialMessages: ChatMessage[] = [
  {
    role: "assistant",
    content: "Hi! Let's put together your Mutual NDA. What's the purpose of this agreement?",
  },
];

export default function NDAChatPanel({
  data,
  onChange,
}: {
  data: NDAFormData;
  onChange: (data: NDAFormData) => void;
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
      const result = await sendNDAChatMessage(nextMessages, data);
      setMessages([...nextMessages, { role: "assistant", content: result.reply }]);
      onChange(result.ndaData);
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
