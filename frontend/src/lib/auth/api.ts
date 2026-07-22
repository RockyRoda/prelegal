import { postJson } from "../postJson";
import type { AuthUser } from "./types";

export function signUp(name: string, email: string): Promise<AuthUser> {
  return postJson("/api/auth/signup", { name, email });
}

export function signIn(email: string): Promise<AuthUser> {
  return postJson("/api/auth/signin", { email });
}
