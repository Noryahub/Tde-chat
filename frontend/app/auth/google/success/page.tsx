"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Loader2 } from "lucide-react";

import { useAuth } from "@/hooks/use-auth";

function GoogleSuccessContent() {
  const searchParams = useSearchParams();
  const { completeGoogleLogin } = useAuth();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const code = searchParams.get("code");

    if (!code) {
      setError("Code Google manquant.");
      return;
    }

    completeGoogleLogin(code).catch((err) => {
      setError(
        err instanceof Error
          ? err.message
          : "Connexion Google impossible."
      );
    });
  }, [completeGoogleLogin, searchParams]);

  if (error) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#f7f8fb] px-4">
        <div className="w-full max-w-md rounded-2xl border bg-white p-6 text-center shadow-sm">
          <h1 className="text-lg font-semibold text-[#111827]">
            Connexion Google impossible
          </h1>
          <p className="mt-2 text-sm text-[#6b7280]">
            {error}
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-[#f7f8fb] px-4">
      <div className="flex items-center gap-3 rounded-2xl border bg-white px-5 py-4 text-sm text-[#374151] shadow-sm">
        <Loader2 className="h-4 w-4 animate-spin text-[#1FA97A]" />
        Connexion Google en cours...
      </div>
    </main>
  );
}

export default function GoogleSuccessPage() {
  return (
    <Suspense fallback={null}>
      <GoogleSuccessContent />
    </Suspense>
  );
}
