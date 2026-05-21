"use client";

import { useState } from "react";
import { usePathname, useRouter } from "next/navigation";

import {
  ChevronLeft,
  ChevronRight,
  LayoutDashboard,
  MessageSquare,
  History,
  Settings,
  LogOut,
} from "lucide-react";

import { cn } from "@/lib/utils";

type SidebarDesktopProps = {
  collapsed: boolean;
  onCollapsedChange: (collapsed: boolean) => void;
};

const items = [
  {
    id: "dashboard",
    label: "Tableau de bord",
    icon: LayoutDashboard,
    href: "/user/dashboard",
  },
  {
    id: "assistant",
    label: "Assistant",
    icon: MessageSquare,
    href: "/user/chat",
  },
  {
    id: "historique",
    label: "Historique",
    icon: History,
    href: "/user/history",
  },
  {
    id: "parametres",
    label: "Paramètres",
    icon: Settings,
    href: "/user/settings",
  },
];

export function SidebarDesktop({
  collapsed,
  onCollapsedChange,
}: SidebarDesktopProps) {

  const router = useRouter();
  const pathname = usePathname();

  // ======================================
  // USER TEMPORAIRE
  // ======================================

  const user = {
    nom: "Betsalel",
    email: "betsalel@tde.tg",
  };

  // ======================================
  // LOGOUT
  // ======================================

  function handleLogout() {

    localStorage.removeItem("token");

    router.push("/login");
  }

  return (

    <aside
      className={cn(
        `
        fixed
        left-0
        top-0
        z-50
        hidden
        h-screen
        border-r
        border-[#e5e7eb]
        bg-white
        transition-all
        duration-300
        lg:flex
        lg:flex-col
        shadow-sm
        `,
        collapsed
          ? "w-[88px]"
          : "w-[280px]"
      )}
    >

      {/* ====================================== */}
      {/* HEADER */}
      {/* ====================================== */}

      <div className="relative flex h-[82px] items-center border-b border-[#f1f1f1] px-5">

        <div className="flex items-center gap-3 overflow-hidden">

          <div
            className="
              flex
              h-11
              w-11
              shrink-0
              items-center
              justify-center
              rounded-2xl
              bg-[#1E8E6A]
              text-white
              shadow-sm
              text-lg
            "
          >

          </div>

          {!collapsed && (

            <div className="min-w-0">

              <h1 className="truncate text-[15px] font-semibold text-[#111827]">
                Assistant TDE
              </h1>

              <p className="truncate text-xs text-[#6b7280]">
                Société Togolaise des Eaux
              </p>

            </div>
          )}
        </div>

        {/* ====================================== */}
        {/* TOGGLE */}
        {/* ====================================== */}

        <button
          onClick={() =>
            onCollapsedChange(!collapsed)
          }
          className="
            absolute
            -right-4
            top-1/2
            flex
            h-9
            w-9
            -translate-y-1/2
            items-center
            justify-center
            rounded-full
            border
            border-[#e5e7eb]
            bg-white
            shadow-md
            transition-all
            hover:scale-105
            hover:bg-[#f9fafb]
          "
        >

          {collapsed ? (
            <ChevronRight className="h-4 w-4 text-[#374151]" />
          ) : (
            <ChevronLeft className="h-4 w-4 text-[#374151]" />
          )}

        </button>

      </div>

      {/* ====================================== */}
      {/* NAVIGATION */}
      {/* ====================================== */}

      <div className="flex-1 px-4 py-6">

        <div className="space-y-2">

          {items.map((item) => {

            const Icon = item.icon;

            const active =
              pathname === item.href;

            return (

              <button
                key={item.id}
                onClick={() =>
                  router.push(item.href)
                }
                className={cn(
                  `
                  flex
                  w-full
                  items-center
                  gap-3
                  rounded-2xl
                  px-4
                  py-3
                  text-sm
                  font-medium
                  transition-all
                  duration-200
                  `,
                  active
                    ? "bg-[#1E8E6A] text-white shadow-sm"
                    : "text-[#374151] hover:bg-[#f3f4f6]"
                )}
              >

                <Icon
                  className={cn(
                    "h-5 w-5 shrink-0",
                    active
                      ? "text-white"
                      : "text-[#6b7280]"
                  )}
                />

                {!collapsed && (
                  <span className="truncate">
                    {item.label}
                  </span>
                )}

              </button>
            );
          })}

        </div>

      </div>

      {/* ====================================== */}
      {/* FOOTER */}
      {/* ====================================== */}

      <div className="border-t border-[#f1f1f1] p-4">

        {/* ====================================== */}
        {/* USER CARD */}
        {/* ====================================== */}

        <div
          className={cn(
            `
            mb-4
            flex
            items-center
            gap-3
            rounded-2xl
            border
            border-[#f1f1f1]
            bg-[#fafafa]
            p-3
            transition-all
            `,
            collapsed && "justify-center"
          )}
        >

          <img
            src={`https://ui-avatars.com/api/?name=${user?.nom || "User"}&background=1E8E6A&color=fff`}
            alt="avatar"
            className="
              h-10
              w-10
              rounded-xl
              object-cover
              shadow-sm
            "
          />

          {!collapsed && (

            <div className="min-w-0 flex-1">

              <p className="truncate text-sm font-semibold text-[#111827]">
                {user?.nom}
              </p>

              <p className="truncate text-xs text-[#6b7280]">
                {user?.email}
              </p>

            </div>
          )}

        </div>

        {/* ====================================== */}
        {/* LOGOUT */}
        {/* ====================================== */}

        <button
          onClick={handleLogout}
          className="
            flex
            w-full
            items-center
            gap-3
            rounded-2xl
            px-4
            py-3
            text-sm
            font-medium
            text-[#dc2626]
            transition-colors
            hover:bg-red-50
          "
        >

          <LogOut className="h-5 w-5 shrink-0" />

          {!collapsed && (
            <span>Déconnexion</span>
          )}

        </button>

      </div>

    </aside>
  );
}