"use client";

import { useEffect, useState } from "react";
import LoginScreen from "@/components/LoginScreen";
import NdaCreatorPage from "@/components/NdaCreatorPage";
import { clearSessionUser, loadSessionUser, saveSessionUser } from "@/lib/auth/session";
import type { AuthUser } from "@/lib/auth/types";

export default function Home() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isSessionLoaded, setIsSessionLoaded] = useState(false);

  useEffect(() => {
    // sessionStorage doesn't exist during SSR, so the session can only be read
    // once mounted on the client.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setUser(loadSessionUser());
    setIsSessionLoaded(true);
  }, []);

  function handleAuthenticated(authUser: AuthUser) {
    saveSessionUser(authUser);
    setUser(authUser);
  }

  function handleSignOut() {
    clearSessionUser();
    setUser(null);
  }

  if (!isSessionLoaded) {
    return null;
  }

  if (!user) {
    return <LoginScreen onAuthenticated={handleAuthenticated} />;
  }

  return <NdaCreatorPage user={user} onSignOut={handleSignOut} />;
}
