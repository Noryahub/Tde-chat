"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/use-auth";
import {
  loadSessionId,
  saveSessionId,
} from "@/storage/chat-storage";

export function LoginForm() {
  const { login, loginWithGoogle } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      await login({ email, password });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Connexion impossible.");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function onGoogleLogin() {
    setError(null);
    setIsSubmitting(true);

    try {
      let sessionId = loadSessionId();

      if (!sessionId) {
        sessionId = `session_${crypto.randomUUID()}`;
        saveSessionId(sessionId);
      }

      await loginWithGoogle(
        sessionId,
        "/user/chat"
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Connexion Google impossible."
      );
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-5">
      <div className="space-y-2">

        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          required
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          className="h-10 w-full rounded-lg border bg-background px-3 text-sm outline-none transition focus:border-foreground focus:ring-2 focus:ring-ring/30"
          placeholder="vous@exemple.com"
        />
      </div>
      <div className="space-y-2">
        <label htmlFor="password" className="text-sm font-medium">
          Mot de passe
        </label>
        <input
          id="password"
          type="password"
          required
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          className="h-10 w-full rounded-lg border bg-background px-3 text-sm outline-none transition focus:border-foreground focus:ring-2 focus:ring-ring/30"
          placeholder="Votre mot de passe"
        />
      </div>
      {error && (
        <p className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
          {error}
        </p>
      )}
        <label htmlFor="email" className="text-sm font-medium">
          Mode invité
        </label>
        <Button
          type="button"
          variant="outline"
          className="h-10 w-full"
          onClick={() => {
            window.location.href = "/user/chat";
          }}
        >
          Continuer en tant qu'invité
        </Button>
      <Button type="submit" className="h-10 w-full" disabled={isSubmitting}>
        {isSubmitting && <Loader2 className="size-4 animate-spin" />}
        Se connecter
      </Button>

      <Button
        type="button"
        variant="outline"
        className="h-10 w-full"
        disabled={isSubmitting}
        onClick={onGoogleLogin}
      >
        <svg className="size-4" viewBox="0 0 24 24">
          <path
            fill="#4285F4"
            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
          />
          <path
            fill="#34A853"
            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
          />
          <path
            fill="#FBBC05"
            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
          />
          <path
            fill="#EA4335"
            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
          />
        </svg>
        Continuer avec Google
      </Button>

      <p className="text-center text-sm text-muted-foreground">
        Pas encore de compte ?{" "}
        <Link href="/register" className="font-medium text-foreground underline-offset-4 hover:underline">
          Creer un compte
        </Link>
      </p>
    </form>
  );
}
