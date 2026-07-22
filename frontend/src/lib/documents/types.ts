export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface DocumentChatReply {
  reply: string;
  docId: string | null;
  documentId: number | null;
  fieldValues: Record<string, string>;
  html: string;
}

export interface DocumentHistoryItem {
  documentId: number;
  docId: string;
  docName: string;
  updatedAt: string;
}

export interface DocumentDetail {
  documentId: number;
  docId: string;
  fieldValues: Record<string, string>;
  html: string;
}
