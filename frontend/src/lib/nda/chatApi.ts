import { postJson } from "../postJson";
import { NDAFormData } from "./types";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface NDAChatReply {
  reply: string;
  ndaData: NDAFormData;
}

export function sendNDAChatMessage(
  messages: ChatMessage[],
  ndaData: NDAFormData
): Promise<NDAChatReply> {
  return postJson("/api/nda/chat", { messages, ndaData });
}
