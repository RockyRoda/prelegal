import { afterEach, describe, expect, it, vi } from "vitest";
import { fetchDocumentDetail, fetchDocumentHistory, sendDocumentChatMessage } from "./api";

describe("documents chat api", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("posts the message history, docId, documentId, and field values with the auth token", async () => {
    const reply = {
      reply: "What's the purpose?",
      docId: "mnda",
      documentId: 7,
      fieldValues: {},
      html: "<article></article>",
    };
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => reply,
    });
    vi.stubGlobal("fetch", fetchMock);

    const messages = [{ role: "user" as const, content: "I need an NDA" }];
    const result = await sendDocumentChatMessage(messages, null, null, {}, "tok_123");

    expect(result).toEqual(reply);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("http://localhost:8000/api/documents/chat");
    expect(JSON.parse(init.body)).toEqual({ messages, docId: null, documentId: null, fieldValues: {} });
    expect(init.headers.Authorization).toBe("Bearer tok_123");
  });

  it("throws the backend's error detail on failure", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ detail: "The assistant had trouble responding." }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(sendDocumentChatMessage([], null, null, {}, "tok_123")).rejects.toThrow(
      "The assistant had trouble responding."
    );
  });
});

describe("document history api", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("fetches the history list with the auth token", async () => {
    const body = { documents: [{ documentId: 1, docId: "mnda", docName: "MNDA", updatedAt: "now" }] };
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => body });
    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchDocumentHistory("tok_123");

    expect(result).toEqual(body);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("http://localhost:8000/api/documents/history");
    expect(init.headers.Authorization).toBe("Bearer tok_123");
  });

  it("fetches a single document's detail", async () => {
    const body = { documentId: 1, docId: "mnda", fieldValues: {}, html: "<article></article>" };
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => body });
    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchDocumentDetail(1, "tok_123");

    expect(result).toEqual(body);
    const [url] = fetchMock.mock.calls[0];
    expect(url).toBe("http://localhost:8000/api/documents/history/1");
  });
});
