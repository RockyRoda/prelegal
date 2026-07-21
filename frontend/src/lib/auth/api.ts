import type { AuthUser } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function postAuth(path: string, body: Record<string, string>): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.detail ?? "Something went wrong. Please try again.");
  }

  return response.json();
}

export function signUp(name: string, email: string): Promise<AuthUser> {
  return postAuth("/api/auth/signup", { name, email });
}

export function signIn(email: string): Promise<AuthUser> {
  return postAuth("/api/auth/signin", { email });
}
