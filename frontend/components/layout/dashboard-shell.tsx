"use client";

import { usePathname } from "next/navigation";

import { AdminSidebar } from "@/components/layout/admin-sidebar";
import { TopNavbar } from "@/components/layout/top-navbar";
import { UserSidebar } from "@/components/layout/user-sidebar";
import { useAuth } from "@/hooks/use-auth";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { isLoading } = useAuth();
  const isAdminArea = pathname.startsWith("/admin");

  if (isLoading) {
    return (
      <div className="grid min-h-screen place-items-center bg-background text-sm text-muted-foreground">
        Chargement...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {isAdminArea ? <AdminSidebar /> : <UserSidebar />}
      <div className="transition-[padding-left] duration-300 ease-in-out sm:pl-[var(--assistant-sidebar-width,280px)]">
        <TopNavbar />
        <main className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          {children}
        </main>
      </div>
    </div>
  );
}
