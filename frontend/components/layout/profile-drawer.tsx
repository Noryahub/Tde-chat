"use client";

import { LogOut, Mail, MoreHorizontal, Shield, UserRound } from "lucide-react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";
import { useAuth } from "@/hooks/use-auth";
import { cn } from "@/lib/utils";

type ProfileDrawerProps = {
  collapsed?: boolean;
};

export function ProfileDrawer({ collapsed = false }: ProfileDrawerProps) {
  const { user, logout } = useAuth();
  const initials =
    user?.name
      .split(" ")
      .map((part) => part[0])
      .join("")
      .slice(0, 2)
      .toUpperCase() ?? "AT";

  return (
    <Drawer direction="right">
      <DrawerTrigger asChild>
        <Button
          variant="ghost"
          className={cn(
            "h-12 w-full justify-start gap-3 rounded-lg px-3",
            collapsed && "justify-center px-0"
          )}
        >
          <Avatar size="sm">
            <AvatarFallback>{initials}</AvatarFallback>
          </Avatar>
          {!collapsed && (
            <>
              <span className="min-w-0 flex-1 text-left">
                <span className="block truncate text-sm font-medium">
                  {user?.name ?? "Assistant TDE"}
                </span>
                <span className="block truncate text-xs text-muted-foreground">
                  {user?.email ?? "session locale"}
                </span>
              </span>
              <MoreHorizontal className="size-4 text-muted-foreground" />
            </>
          )}
        </Button>
      </DrawerTrigger>
      <DrawerContent className="max-w-sm">
        <DrawerHeader className="border-b">
          <DrawerTitle>Profil</DrawerTitle>
        </DrawerHeader>
        <div className="space-y-4 p-4">
          <div className="flex items-center gap-3 rounded-lg border bg-card p-3">
            <Avatar>
              <AvatarFallback>{initials}</AvatarFallback>
            </Avatar>
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold">{user?.name}</p>
              <p className="truncate text-xs text-muted-foreground">{user?.email}</p>
            </div>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-3 rounded-lg px-2 py-2 text-muted-foreground">
              <UserRound className="size-4" />
              <span>ID utilisateur: {user?.id}</span>
            </div>
            <div className="flex items-center gap-3 rounded-lg px-2 py-2 text-muted-foreground">
              <Shield className="size-4" />
              <span className="capitalize">Role: {user?.role}</span>
            </div>
            <div className="flex items-center gap-3 rounded-lg px-2 py-2 text-muted-foreground">
              <Mail className="size-4" />
              <span className="truncate">{user?.email}</span>
            </div>
          </div>
        </div>
        <DrawerFooter className="border-t">
          <DrawerClose asChild>
            <Button variant="outline" onClick={logout} className="justify-start gap-2">
              <LogOut className="size-4" />
              Deconnexion
            </Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  );
}
