"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { SidebarItem } from "@/types";

type SidebarButtonProps = {
  item: SidebarItem;
  collapsed?: boolean;
  onNavigate?: () => void;
};

function isActiveRoute(pathname: string, href: string) {
  return pathname === href || pathname.startsWith(`${href}/`);
}

export function SidebarButton({ item, collapsed = false, onNavigate }: SidebarButtonProps) {
  const pathname = usePathname();
  const Icon = item.icon;
  const active = isActiveRoute(pathname, item.href);

  return (
    <Button
      asChild
      variant={active ? "secondary" : "ghost"}
      className={cn(
        "h-10 w-full justify-start gap-3 rounded-lg px-3 text-muted-foreground transition-colors",
        active && "bg-foreground text-background hover:bg-foreground/90 hover:text-background",
        collapsed && "justify-center px-0"
      )}
      title={collapsed ? item.title : undefined}
    >
      <Link href={item.href} onClick={onNavigate}>
        <Icon className="size-4" />
        {!collapsed && (
          <>
            <span className="min-w-0 flex-1 truncate text-left">{item.title}</span>
            {item.badge && (
              <span className="rounded-full bg-muted px-2 py-0.5 text-xs text-muted-foreground">
                {item.badge}
              </span>
            )}
          </>
        )}
      </Link>
    </Button>
  );
}
