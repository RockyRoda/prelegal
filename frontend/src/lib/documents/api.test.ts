import { afterEach, describe, expect, it, vi } from "vitest";
import { sendDocumentChatMessage } from "./api";

describe("documents chat api", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("posts the message history, docId, and field values", async () => {
    const reply = { reply: "What's the purpose?", docId: "mnda", fieldValues: {}, html: "<article></article>" };
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => reply,
    });
    vi.stubGlobal("fetch", fetchMock);

    const messages = [{ role: "user" as const, content: "I need an NDA" }];
    const result = await sendDocumentChatMessage(messages, null, {});

    expect(result).toEqual(reply);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("http://localhost:8000/api/documents/chat");
    expect(JSON.parse(init.body)).toEqual({ messages, docId: null, fieldValues: {} });
  });

  it("throws the backend's error detail on failure", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ detail: "The assistant had trouble responding." }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(sendDocumentChatMessage([], null, {})).rejects.toThrow(
      "The assistant had trouble responding."
    );
  });
});
