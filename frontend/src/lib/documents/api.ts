import { getJson, postJson } from "../postJson";
import type { ChatMessage, DocumentChatReply, DocumentDetail, DocumentHistoryItem } from "./types";

export function sendDocumentChatMessage(
  messages: ChatMessage[],
  docId: string | null,
  documentId: number | null,
  fieldValues: Record<string, string>,
  token: string
): Promise<DocumentChatReply> {
  return postJson("/api/documents/chat", { messages, docId, documentId, fieldValues }, token);
}

export function fetchDocumentHistory(token: string): Promise<{ documents: DocumentHistoryItem[] }> {
  return getJson("/api/documents/history", token);
}

export function fetchDocumentDetail(documentId: number, token: string): Promise<DocumentDetail> {
  return getJson(`/api/documents/history/${documentId}`, token);
}
