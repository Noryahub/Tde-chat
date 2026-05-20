"use client";

import { useEffect, useState } from "react";

import { useMediaQuery } from "@/hooks/use-media-query";
import type { SidebarSection, UserRole } from "@/types";

import { SidebarDesktop } from "./sidebar-desktop";
import { SidebarMobile } from "./sidebar-mobile";

type SidebarProps = {
  role: UserRole;
  sections: SidebarSection[];
};

export function Sidebar({ role, sections }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false);
  const isDesktop = useMediaQuery("(min-width: 640px)", {
    initializeWithValue: false,
  });

  useEffect(() => {
    document.documentElement.style.setProperty(
      "--assistant-sidebar-width",
      isDesktop ? (collapsed ? "76px" : "280px") : "0px"
    );
  }, [collapsed, isDesktop]);

  if (isDesktop) {
    return (
      <SidebarDesktop
        collapsed={collapsed}
        onCollapsedChange={setCollapsed}
        role={role}
        sections={sections}
      />
    );
  }

  return <SidebarMobile role={role} sections={sections} />;
}
