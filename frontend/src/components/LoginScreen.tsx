"use client";

import { useState, type FormEvent } from "react";
import { signIn, signUp } from "@/lib/auth/api";
import type { AuthUser } from "@/lib/auth/types";

interface LoginScreenProps {
  onAuthenticated: (user: AuthUser) => void;
}

type Mode = "signin" | "signup";

export default function LoginScreen({ onAuthenticated }: LoginScreenProps) {
  const [mode, setMode] = useState<Mode>("signin");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const user = mode === "signup" ? await signUp(name, email) : await signIn(email);
      onAuthenticated(user);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 px-6">
      <div className="w-full max-w-sm rounded-lg border-t-4 border-[#ecad0a] bg-white p-8 shadow-sm">
        <h1 className="text-xl font-semibold text-[#032147]">Prelegal</h1>
        <p className="mt-1 text-sm text-[#888888]">
          {mode === "signup" ? "Create an account to continue." : "Sign in to continue."}
        </p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          {mode === "signup" && (
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-[#888888]">
                Name
              </label>
              <input
                id="name"
                type="text"
                required
                value={name}
                onChange={(event) => setName(event.target.value)}
                className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm focus:border-[#209dd7] focus:outline-none"
              />
            </div>
          )}

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-[#888888]">
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm focus:border-[#209dd7] focus:outline-none"
            />
          </div>

          {error && <p className="text-sm text-red-600">{error}</p>}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-md bg-[#753991] px-4 py-2.5 text-sm font-medium text-white hover:bg-[#5f2e75] disabled:opacity-50"
          >
            {isSubmitting ? "Please wait…" : mode === "signup" ? "Sign up" : "Sign in"}
          </button>
        </form>

        <button
          type="button"
          onClick={() => {
            setError(null);
            setMode(mode === "signup" ? "signin" : "signup");
          }}
          className="mt-4 text-sm text-[#209dd7] hover:underline"
        >
          {mode === "signup" ? "Already have an account? Sign in" : "Need an account? Sign up"}
        </button>
      </div>
    </div>
  );
}
