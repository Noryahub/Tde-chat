"use client";

import { SheetClose } from "@/components/ui/sheet";
import type { SidebarItem } from "@/types";

import { SidebarButton } from "./sidebar-button";

export function SidebarButtonSheet({ item }: { item: SidebarItem }) {
  return (
    <SheetClose asChild>
      <SidebarButton item={item} />
    </SheetClose>
  );
}
