import { postJson } from "../postJson";
import type { AuthSession } from "./types";

export function signUp(name: string, email: string, password: string): Promise<AuthSession> {
  return postJson("/api/auth/signup", { name, email, password });
}

export function signIn(email: string, password: string): Promise<AuthSession> {
  return postJson("/api/auth/signin", { email, password });
}
