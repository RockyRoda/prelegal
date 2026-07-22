import { beforeEach, describe, expect, it } from "vitest";
import { clearSession, loadSession, saveSession } from "./session";

describe("session", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("returns null when nothing is stored", () => {
    expect(loadSession()).toBeNull();
  });

  it("round-trips a saved session", () => {
    const session = { user: { id: 1, name: "Ada Lovelace", email: "ada@example.com" }, token: "tok_123" };
    saveSession(session);
    expect(loadSession()).toEqual(session);
  });

  it("returns null instead of throwing on corrupt stored data", () => {
    localStorage.setItem("prelegal.session", "not valid json");
    expect(loadSession()).toBeNull();
  });

  it("removes the stored session on clear", () => {
    saveSession({ user: { id: 1, name: "Ada Lovelace", email: "ada@example.com" }, token: "tok_123" });
    clearSession();
    expect(loadSession()).toBeNull();
  });
});
