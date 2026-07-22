import { postJson } from "../postJson";
import type { ChatMessage, DocumentChatReply } from "./types";

export function sendDocumentChatMessage(
  messages: ChatMessage[],
  docId: string | null,
  fieldValues: Record<string, string>
): Promise<DocumentChatReply> {
  return postJson("/api/documents/chat", { messages, docId, fieldValues });
}
