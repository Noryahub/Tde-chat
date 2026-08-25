"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Loader2 } from "lucide-react";

import { useAuth } from "@/hooks/use-auth";

function GoogleSuccessContent() {
  const searchParams = useSearchParams();
  const { completeGoogleLogin } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const exchangedRef = useRef(false);
  const code = searchParams.get("code");

  useEffect(() => {
    if (!code || exchangedRef.current) {
      return;
    }

    exchangedRef.current = true;

    completeGoogleLogin(code)
      .catch((err) => {
        setError(
          err instanceof Error
            ? err.message
            : "Connexion Google impossible."
        );
      });
  }, [completeGoogleLogin, searchParams, code]);

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

  if (!code) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#f7f8fb] px-4">
        <div className="w-full max-w-md rounded-2xl border bg-white p-6 text-center shadow-sm">
          <h1 className="text-lg font-semibold text-[#111827]">
            Connexion Google impossible
          </h1>
          <p className="mt-2 text-sm text-[#6b7280]">
            Code Google manquant.
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
