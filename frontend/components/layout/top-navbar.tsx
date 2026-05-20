"use client";

import { Bell, Search } from "lucide-react";
import { usePathname } from "next/navigation";

import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/use-auth";

const titles: Record<string, string> = {
  "/admin/dashboard": "Dashboard admin",
  "/admin/analytics": "Analytics",
  "/admin/users": "Utilisateurs",
  "/admin/signalements": "Signalements",
  "/admin/settings": "Parametres",
  "/user/chat": "Chat TDE",
  "/user/history": "Historique",
  "/user/profile": "Profil",
};

export function TopNavbar() {
  const pathname = usePathname();
  const { user } = useAuth();

  return (
    <header className="sticky top-0 z-30 border-b border-border/80 bg-background/80 backdrop-blur">
      <div className="flex h-16 items-center gap-3 px-4 sm:px-6">
        <div className="ml-11 min-w-0 flex-1 sm:ml-0">
          <p className="truncate text-sm font-semibold">
            {titles[pathname] ?? "Assistant TDE"}
          </p>
          <p className="truncate text-xs text-muted-foreground">
            Connecte en tant que {user?.role ?? "utilisateur"}
          </p>
        </div>
        <div className="hidden h-9 min-w-[240px] items-center gap-2 rounded-lg border bg-muted/40 px-3 text-sm text-muted-foreground md:flex">
          <Search className="size-4" />
          <span>Rechercher...</span>
        </div>
        <Button variant="outline" size="icon" aria-label="Notifications">
          <Bell className="size-4" />
        </Button>
      </div>
    </header>
  );
}
