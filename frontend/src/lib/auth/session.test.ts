import { beforeEach, describe, expect, it } from "vitest";
import { clearSessionUser, loadSessionUser, saveSessionUser } from "./session";

describe("session", () => {
  beforeEach(() => {
    sessionStorage.clear();
  });

  it("returns null when nothing is stored", () => {
    expect(loadSessionUser()).toBeNull();
  });

  it("round-trips a saved user", () => {
    const user = { id: 1, name: "Ada Lovelace", email: "ada@example.com" };
    saveSessionUser(user);
    expect(loadSessionUser()).toEqual(user);
  });

  it("returns null instead of throwing on corrupt stored data", () => {
    sessionStorage.setItem("prelegal.user", "not valid json");
    expect(loadSessionUser()).toBeNull();
  });

  it("removes the stored user on clear", () => {
    saveSessionUser({ id: 1, name: "Ada Lovelace", email: "ada@example.com" });
    clearSessionUser();
    expect(loadSessionUser()).toBeNull();
  });
});
