import {
  BarChart3,
  Gauge,
  Settings,
  ShieldAlert,
  UsersRound,
} from "lucide-react";

import type { SidebarSection } from "@/types";

export const adminSidebarItems: SidebarSection[] = [
  {
    title: "Pilotage",
    items: [
      {
        title: "Dashboard",
        href: "/admin/dashboard",
        icon: Gauge,
      },
      {
        title: "Analytics",
        href: "/admin/analytics",
        icon: BarChart3,
      },
    ],
  },
  {
    title: "Administration",
    items: [
      {
        title: "Utilisateurs",
        href: "/admin/users",
        icon: UsersRound,
      },
      {
        title: "Signalements",
        href: "/admin/signalements",
        icon: ShieldAlert,
        badge: "12",
      },
      {
        title: "Parametres",
        href: "/admin/settings",
        icon: Settings,
      },
    ],
  },
];
