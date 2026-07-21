import type { AuthUser } from "./types";

const SESSION_KEY = "prelegal.user";

export function loadSessionUser(): AuthUser | null {
  const raw = sessionStorage.getItem(SESSION_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as AuthUser;
  } catch {
    return null;
  }
}

export function saveSessionUser(user: AuthUser): void {
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(user));
}

export function clearSessionUser(): void {
  sessionStorage.removeItem(SESSION_KEY);
}
