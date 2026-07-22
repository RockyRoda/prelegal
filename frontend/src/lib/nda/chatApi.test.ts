import { afterEach, describe, expect, it, vi } from "vitest";
import { sendNDAChatMessage } from "./chatApi";
import { defaultNDAFormData } from "./defaults";

describe("nda chat api", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("posts the message history and current NDA data", async () => {
    const ndaData = defaultNDAFormData();
    const reply = { reply: "What's the purpose?", ndaData };
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => reply,
    });
    vi.stubGlobal("fetch", fetchMock);

    const messages = [{ role: "user" as const, content: "Hi" }];
    const result = await sendNDAChatMessage(messages, ndaData);

    expect(result).toEqual(reply);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("http://localhost:8000/api/nda/chat");
    expect(JSON.parse(init.body)).toEqual({ messages, ndaData });
  });

  it("throws the backend's error detail on failure", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ detail: "The model call failed" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(sendNDAChatMessage([], defaultNDAFormData())).rejects.toThrow(
      "The model call failed"
    );
  });

  it("falls back to a generic message when the error body isn't JSON", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => {
        throw new Error("not json");
      },
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(sendNDAChatMessage([], defaultNDAFormData())).rejects.toThrow(
      "Something went wrong. Please try again."
    );
  });
});
