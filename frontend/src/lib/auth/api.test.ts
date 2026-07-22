import { afterEach, describe, expect, it, vi } from "vitest";
import { signIn, signUp } from "./api";

describe("auth api", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("signUp posts name, email, and password and returns the session", async () => {
    const session = { user: { id: 1, name: "Ada Lovelace", email: "ada@example.com" }, token: "tok_123" };
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => session,
    });
    vi.stubGlobal("fetch", fetchMock);

    const result = await signUp("Ada Lovelace", "ada@example.com", "hunter22");

    expect(result).toEqual(session);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("http://localhost:8000/api/auth/signup");
    expect(JSON.parse(init.body)).toEqual({
      name: "Ada Lovelace",
      email: "ada@example.com",
      password: "hunter22",
    });
  });

  it("signIn posts email and password", async () => {
    const session = { user: { id: 1, name: "Ada Lovelace", email: "ada@example.com" }, token: "tok_123" };
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => session,
    });
    vi.stubGlobal("fetch", fetchMock);

    await signIn("ada@example.com", "hunter22");

    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("http://localhost:8000/api/auth/signin");
    expect(JSON.parse(init.body)).toEqual({ email: "ada@example.com", password: "hunter22" });
  });

  it("throws the backend's error detail on failure", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ detail: "Invalid email or password" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(signIn("nobody@example.com", "wrong")).rejects.toThrow(
      "Invalid email or password"
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

    await expect(signIn("nobody@example.com", "wrong")).rejects.toThrow(
      "Something went wrong. Please try again."
    );
  });
});
