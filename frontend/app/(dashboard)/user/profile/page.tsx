"use client";

import { useAuth } from "@/hooks/use-auth";

export default function UserProfilePage() {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Profil</h1>
        <p className="mt-1 text-sm text-muted-foreground">Informations de votre compte.</p>
      </div>
      <section className="max-w-xl rounded-lg border bg-card p-5">
        <div className="space-y-4 text-sm">
          <p className="flex justify-between gap-4"><span className="text-muted-foreground">Nom</span><strong>{user?.name}</strong></p>
          <p className="flex justify-between gap-4"><span className="text-muted-foreground">Email</span><strong>{user?.email}</strong></p>
          <p className="flex justify-between gap-4"><span className="text-muted-foreground">Role</span><strong>{user?.role}</strong></p>
        </div>
      </section>
    </div>
  );
}
