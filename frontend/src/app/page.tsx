"use client";

import { useEffect, useState } from "react";
import LoginScreen from "@/components/LoginScreen";
import DocumentCreatorPage from "@/components/DocumentCreatorPage";
import { clearSession, loadSession, saveSession } from "@/lib/auth/session";
import type { AuthSession } from "@/lib/auth/types";

export default function Home() {
  const [session, setSession] = useState<AuthSession | null>(null);
  const [isSessionLoaded, setIsSessionLoaded] = useState(false);

  useEffect(() => {
    // localStorage doesn't exist during SSR, so the session can only be read
    // once mounted on the client.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setSession(loadSession());
    setIsSessionLoaded(true);
  }, []);

  function handleAuthenticated(authSession: AuthSession) {
    saveSession(authSession);
    setSession(authSession);
  }

  function handleSignOut() {
    clearSession();
    setSession(null);
  }

  if (!isSessionLoaded) {
    return null;
  }

  if (!session) {
    return <LoginScreen onAuthenticated={handleAuthenticated} />;
  }

  return <DocumentCreatorPage session={session} onSignOut={handleSignOut} />;
}
