"use client";
import { useState } from "react";
import { usePathname } from "next/navigation";
import { AdminSidebar } from "@/components/layout/admin-sidebar";
import { GuestSidebar } from "@/components/layout/guest-sidebar";
import { TopNavbar } from "@/components/layout/top-navbar";
import { UserSidebar } from "@/components/layout/user-sidebar";
import { SidebarMobile } from "@/components/layout/sidebar-mobile";
import { useAuth } from "@/hooks/use-auth";
import { adminSidebarItems } from "@/config/admin-sidebar-items";
import { userSidebarItems } from "@/config/user-sidebar-items";
import { guestSidebarItems } from "@/config/guest-sidebar-items";
export function DashboardShell({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const {
    isLoading,
    isAuthenticated,
    role,
  } = useAuth();

  const [mobileSidebarOpen,
    setMobileSidebarOpen] =
    useState(false);

  const isAdminArea =
    pathname.startsWith("/admin");

  if (isLoading) {
    return (
      <div
        className="
          grid
          min-h-screen
          place-items-center
          bg-background
          text-sm
          text-muted-foreground
        "
      >
        Chargement...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* SIDEBAR DESKTOP */}
      {isAdminArea ? (
        <AdminSidebar />
      ) : isAuthenticated ? (
        <UserSidebar />
      ) : (
        <GuestSidebar />
      )}

      {/* SIDEBAR MOBILE */}

     <SidebarMobile
          role={role}
          sections={
            isAdminArea
              ? adminSidebarItems
              : isAuthenticated
                ? userSidebarItems
                : guestSidebarItems
          }
          open={mobileSidebarOpen}
          onOpenChange={setMobileSidebarOpen}
        />
      {/* CONTENU */}
      <div
        className="
          transition-[padding-left]
          duration-300
          ease-in-out
          lg:pl-[var(--assistant-sidebar-width,280px)]
        "
      >
        <TopNavbar
          onMenuClick={() =>
            setMobileSidebarOpen(true)
          }
        />
        <main
          className="
            mx-auto
            w-full
            max-w-7xl
            px-4
            py-6
            sm:px-6
            lg:px-8
          "
        >
          {children}
        </main>
      </div>
    </div>
  );
}