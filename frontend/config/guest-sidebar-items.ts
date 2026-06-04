import {
  MessageSquare,
  LogIn,
  UserPlus
} from "lucide-react";

export const guestSidebarItems = [
  {
    items: [
      {
        title: "Chat",
        href: "/user/chat",
        icon: MessageSquare,
      },
      {
        title: "Connexion",
        href: "/login",
        icon: LogIn,
      },
      {
        title: "Inscription",
        href: "/register",
        icon: UserPlus,
      },
    ],
  },
];