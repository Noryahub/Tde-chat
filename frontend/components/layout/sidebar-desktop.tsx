"use client";

import { ChevronLeft, ChevronRight, GraduationCap } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";
import type { SidebarSection, UserRole } from "@/types";

import { ProfileDrawer } from "./profile-drawer";
import { SidebarButton } from "./sidebar-button";

type SidebarDesktopProps = {
  role: UserRole;
  sections: SidebarSection[];
  collapsed: boolean;
  onCollapsedChange: (collapsed: boolean) => void;
};

export function SidebarDesktop({
  role,
  sections,
  collapsed,
  onCollapsedChange,
}: SidebarDesktopProps) {
  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-40 hidden border-r border-border/80 bg-sidebar/95 backdrop-blur supports-[backdrop-filter]:bg-sidebar/80 sm:flex sm:flex-col",
        "transition-[width] duration-300 ease-in-out",
        collapsed ? "w-[76px]" : "w-[280px]"
      )}
    >
      <div className="flex h-16 items-center gap-3 px-4">
        <div className="grid size-9 place-items-center rounded-lg bg-foreground text-background">
          <GraduationCap className="size-5" />
        </div>
        {!collapsed && (
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold">Assistant TDE</p>
            <p className="truncate text-xs capitalize text-muted-foreground">{role}</p>
          </div>
        )}
      </div>

      <nav className="flex-1 space-y-6 overflow-y-auto px-3 py-4">
        {sections.map((section, sectionIndex) => (
          <div key={section.title ?? sectionIndex} className="space-y-2">
            {section.title && !collapsed && (
              <p className="px-3 text-xs font-medium uppercase tracking-wide text-muted-foreground">
                {section.title}
              </p>
            )}
            <div className="space-y-1">
              {section.items.map((item) => (
                <SidebarButton key={item.href} item={item} collapsed={collapsed} />
              ))}
            </div>
          </div>
        ))}
      </nav>

      <div className="p-3">
        <Separator className="mb-3" />
        <ProfileDrawer collapsed={collapsed} />
        <Button
          variant="ghost"
          size="icon"
          className="absolute -right-4 top-20 size-8 rounded-full border bg-background shadow-sm"
          onClick={() => onCollapsedChange(!collapsed)}
          aria-label={collapsed ? "Etendre le menu" : "Reduire le menu"}
        >
          {collapsed ? <ChevronRight className="size-4" /> : <ChevronLeft className="size-4" />}
        </Button>
      </div>
    </aside>
  );
}
