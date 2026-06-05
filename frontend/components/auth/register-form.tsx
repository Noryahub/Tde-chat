"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/use-auth";

export function RegisterForm() {
  const { register } = useAuth();
  const [nom, setNom] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      await register({ nom, email, password });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Inscription impossible.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-5">
      <div className="space-y-2">
        <label htmlFor="nom" className="text-sm font-medium">
          Nom
        </label>
        <input
          id="nom"
          required
          value={nom}
          onChange={(event) => setNom(event.target.value)}
          className="h-10 w-full rounded-lg border bg-background px-3 text-sm outline-none transition focus:border-foreground focus:ring-2 focus:ring-ring/30"
          placeholder="Votre nom"
        />
      </div>
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
          minLength={6}
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          className="h-10 w-full rounded-lg border bg-background px-3 text-sm outline-none transition focus:border-foreground focus:ring-2 focus:ring-ring/30"
          placeholder="6 caracteres minimum"
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
        Creer le compte
      </Button>
      <p className="text-center text-sm text-muted-foreground">
        Deja inscrit ?{" "}
        <Link href="/login" className="font-medium text-foreground underline-offset-4 hover:underline">
          Se connecter
        </Link>
      </p>

    </form>
  );
}
