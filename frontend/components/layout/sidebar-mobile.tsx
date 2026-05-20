"use client";

import { GraduationCap, Menu } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Separator } from "@/components/ui/separator";
import type { SidebarSection, UserRole } from "@/types";

import { ProfileDrawer } from "./profile-drawer";
import { SidebarButtonSheet } from "./sidebar-button-sheet";

type SidebarMobileProps = {
  role: UserRole;
  sections: SidebarSection[];
};

export function SidebarMobile({ role, sections }: SidebarMobileProps) {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="fixed left-4 top-4 z-50 sm:hidden"
          aria-label="Ouvrir le menu"
        >
          <Menu className="size-5" />
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-[300px] p-0" showCloseButton>
        <SheetHeader className="border-b px-4 py-4 text-left">
          <SheetTitle className="flex items-center gap-3">
            <span className="grid size-9 place-items-center rounded-lg bg-foreground text-background">
              <GraduationCap className="size-5" />
            </span>
            <span>
              <span className="block text-sm font-semibold">Assistant TDE</span>
              <span className="block text-xs capitalize text-muted-foreground">{role}</span>
            </span>
          </SheetTitle>
        </SheetHeader>

        <nav className="flex-1 space-y-6 overflow-y-auto px-3 py-4">
          {sections.map((section, sectionIndex) => (
            <div key={section.title ?? sectionIndex} className="space-y-2">
              {section.title && (
                <p className="px-3 text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  {section.title}
                </p>
              )}
              <div className="space-y-1">
                {section.items.map((item) => (
                  <SidebarButtonSheet key={item.href} item={item} />
                ))}
              </div>
            </div>
          ))}
        </nav>

        <div className="mt-auto p-3">
          <Separator className="mb-3" />
          <ProfileDrawer />
        </div>
      </SheetContent>
    </Sheet>
  );
}
