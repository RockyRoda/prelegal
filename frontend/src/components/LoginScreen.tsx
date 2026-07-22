"use client";

import { useState, type FormEvent } from "react";
import { signIn, signUp } from "@/lib/auth/api";
import type { AuthSession } from "@/lib/auth/types";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";

interface LoginScreenProps {
  onAuthenticated: (session: AuthSession) => void;
}

type Mode = "signin" | "signup";

export default function LoginScreen({ onAuthenticated }: LoginScreenProps) {
  const [mode, setMode] = useState<Mode>("signin");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const session = mode === "signup" ? await signUp(name, email, password) : await signIn(email, password);
      onAuthenticated(session);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 px-6 dark:bg-zinc-950">
      <Card className="w-full max-w-sm border-t-4 border-brand-yellow p-8">
        <h1 className="text-xl font-semibold text-brand-navy dark:text-zinc-50">Prelegal</h1>
        <p className="mt-1 text-sm text-brand-gray">
          {mode === "signup" ? "Create an account to continue." : "Sign in to continue."}
        </p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          {mode === "signup" && (
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-brand-gray">
                Name
              </label>
              <Input
                id="name"
                type="text"
                required
                value={name}
                onChange={(event) => setName(event.target.value)}
                className="mt-1"
              />
            </div>
          )}

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-brand-gray">
              Email
            </label>
            <Input
              id="email"
              type="email"
              required
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="mt-1"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-brand-gray">
              Password
            </label>
            <Input
              id="password"
              type="password"
              required
              minLength={mode === "signup" ? 8 : undefined}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="mt-1"
            />
            {mode === "signup" && <p className="mt-1 text-xs text-brand-gray">At least 8 characters.</p>}
          </div>

          {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}

          <Button type="submit" disabled={isSubmitting} className="w-full">
            {isSubmitting ? "Please wait…" : mode === "signup" ? "Sign up" : "Sign in"}
          </Button>
        </form>

        <button
          type="button"
          onClick={() => {
            setError(null);
            setMode(mode === "signup" ? "signin" : "signup");
          }}
          className="mt-4 text-sm text-brand-blue hover:underline"
        >
          {mode === "signup" ? "Already have an account? Sign in" : "Need an account? Sign up"}
        </button>
      </Card>
    </div>
  );
}
