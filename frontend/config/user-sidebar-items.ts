import { History, MessageSquareText, UserRound, Plus } from "lucide-react";

import type { SidebarSection } from "@/types";

export const userSidebarItems: SidebarSection[] = [
  {
    title: "Assistant",
    items: [
        {
            title: "Nouvelle conversation",
            href:"#",
            icon: Plus,
        },
      {
        title: "Chat TDE",
        href: "/user/chat",
        icon: MessageSquareText,
      },

      {
        title: "Profil",
        href: "/user/profile",
        icon: UserRound,
      },
    ],
  },
];
