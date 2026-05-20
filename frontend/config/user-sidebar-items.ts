import { History, MessageSquareText, UserRound } from "lucide-react";

import type { SidebarSection } from "@/types";

export const userSidebarItems: SidebarSection[] = [
  {
    title: "Assistant",
    items: [
      {
        title: "Chat TDE",
        href: "/user/chat",
        icon: MessageSquareText,
      },
      {
        title: "Historique",
        href: "/user/history",
        icon: History,
      },
      {
        title: "Profil",
        href: "/user/profile",
        icon: UserRound,
      },
    ],
  },
];
