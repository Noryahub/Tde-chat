"use client";

import { createContext, useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import {
  exchangeGoogleLogin,
  login as loginRequest,
  register as registerRequest,
  startGoogleLogin,
} from "@/services/auth-service";
import type { AuthSession, AuthUser, LoginPayload, RegisterPayload, UserRole } from "@/types";
import { clearChatStorage } from "@/storage/chat-storage";

type AuthContextValue = {
  user: AuthUser | null;
  token: string | null;
  role: UserRole | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  loginWithGoogle: (sessionId: string, redirectPath?: string) => Promise<void>;
  completeGoogleLogin: (code: string) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => void;
};

export const AuthContext = createContext<AuthContextValue | null>(null);

const STORAGE_KEY = "assistant-tde-session";

function setCookie(name: string, value: string, maxAge = 60 * 60 * 24 * 7) {
  document.cookie = `${name}=${encodeURIComponent(value)}; path=/; max-age=${maxAge}; samesite=lax`;
}

function clearCookie(name: string) {
  document.cookie = `${name}=; path=/; max-age=0; samesite=lax`;
}

function persistSession(session: AuthSession) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
  setCookie("assistant_tde_token", session.token);
  setCookie("assistant_tde_role", session.user.role);
}

function clearSession() {
  localStorage.removeItem(STORAGE_KEY);
  clearCookie("assistant_tde_token");
  clearCookie("assistant_tde_role");
}

function getStoredSession(): AuthSession | null {
  try {
    const value = localStorage.getItem(STORAGE_KEY);
    return value ? (JSON.parse(value) as AuthSession) : null;
  } catch {
    clearSession();
    return null;
  }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [session, setSession] = useState<AuthSession | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedSession = getStoredSession();
    if (storedSession) {
      setSession(storedSession);
      persistSession(storedSession);
    }
    setIsLoading(false);
  }, []);

  const login = useCallback(
    async (payload: LoginPayload) => {
      const nextSession = await loginRequest(payload);
      persistSession(nextSession);
      setSession(nextSession);
      router.replace(
        nextSession.user.role === "admin" ? "/admin/dashboard" : "/user/chat"
      );
    },
    [router]
  );

  const register = useCallback(
    async (payload: RegisterPayload) => {
      await registerRequest(payload);
      router.replace("/login");
    },
    [router]
  );

  const loginWithGoogle = useCallback(
    async (
      sessionId: string,
      redirectPath = "/user/chat"
    ) => {
      const response = await startGoogleLogin(
        sessionId,
        redirectPath
      );

      window.location.href = response.auth_url;
    },
    []
  );

  const completeGoogleLogin = useCallback(
    async (code: string) => {
      const nextSession = await exchangeGoogleLogin(code);
      persistSession(nextSession);
      setSession(nextSession);
      router.replace("/user/chat");
    },
    [router]
  );

  const logout = useCallback(async () => {

  // Suppression de la session utilisateur
  clearSession();

  // Suppression des données du chatbot
  await clearChatStorage(false);

  // Réinitialisation du contexte
  setSession(null);

  // Retour vers le chatbot en mode anonyme
  window.location.href = "/user/chat";

}, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user: session?.user ?? null,
      token: session?.token ?? null,
      role: session?.user.role ?? null,
      isAuthenticated: Boolean(session?.token),
      isLoading,
      login,
      loginWithGoogle,
      completeGoogleLogin,
      register,
      logout,
    }),
    [
      completeGoogleLogin,
      isLoading,
      login,
      loginWithGoogle,
      logout,
      register,
      session,
    ]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
