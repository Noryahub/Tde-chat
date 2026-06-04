"use client";

import { guestSidebarItems }
from "@/config/guest-sidebar-items";

import { Sidebar } from "./sidebar";

export function GuestSidebar() {
  return (
    <Sidebar
      role="user"
      sections={guestSidebarItems}
    />
  );
}