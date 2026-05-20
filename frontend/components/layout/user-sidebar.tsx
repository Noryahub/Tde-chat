"use client";

import { userSidebarItems } from "@/config/user-sidebar-items";

import { Sidebar } from "./sidebar";

export function UserSidebar() {
  return <Sidebar role="user" sections={userSidebarItems} />;
}
