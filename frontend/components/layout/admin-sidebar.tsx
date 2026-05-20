"use client";

import { adminSidebarItems } from "@/config/admin-sidebar-items";

import { Sidebar } from "./sidebar";

export function AdminSidebar() {
  return <Sidebar role="admin" sections={adminSidebarItems} />;
}
