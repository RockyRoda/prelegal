import { afterEach, describe, expect, it, vi } from "vitest";
import { signIn, signUp } from "./api";

describe("auth api", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("signUp posts name and email and returns the created user", async () => {
    const user = { id: 1, name: "Ada Lovelace", email: "ada@example.com" };
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => user,
    });
    vi.stubGlobal("fetch", fetchMock);

    const result = await signUp("Ada Lovelace", "ada@example.com");

    expect(result).toEqual(user);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("http://localhost:8000/api/auth/signup");
    expect(JSON.parse(init.body)).toEqual({ name: "Ada Lovelace", email: "ada@example.com" });
  });

  it("signIn posts only the email", async () => {
    const user = { id: 1, name: "Ada Lovelace", email: "ada@example.com" };
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => user,
    });
    vi.stubGlobal("fetch", fetchMock);

    await signIn("ada@example.com");

    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("http://localhost:8000/api/auth/signin");
    expect(JSON.parse(init.body)).toEqual({ email: "ada@example.com" });
  });

  it("throws the backend's error detail on failure", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ detail: "No account found for this email" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(signIn("nobody@example.com")).rejects.toThrow(
      "No account found for this email"
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

    await expect(signIn("nobody@example.com")).rejects.toThrow(
      "Something went wrong. Please try again."
    );
  });
});
