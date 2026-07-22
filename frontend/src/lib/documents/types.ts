export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface DocumentChatReply {
  reply: string;
  docId: string | null;
  fieldValues: Record<string, string>;
  html: string;
}
