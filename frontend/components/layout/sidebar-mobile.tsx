"use client";

import {
  GraduationCap,
  LogOut,
} from "lucide-react";

import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";

import {
  Avatar,
  AvatarFallback,
} from "@/components/ui/avatar";

import { useAuth } from "@/hooks/use-auth";

import type {
  SidebarSection,
  UserRole,
} from "@/types";

import { SidebarButtonSheet } from "./sidebar-button-sheet";

type SidebarMobileProps = {
  role: UserRole;
  sections: SidebarSection[];
  open: boolean;
  onOpenChange: (
    open: boolean
  ) => void;
};

export function SidebarMobile({
  role,
  sections,
  open,
  onOpenChange,
}: SidebarMobileProps) {

  const {
    user,
    logout,
  } = useAuth();

  const displayName =
    user?.nom ||
    user?.name ||
    "Utilisateur";

  const initials =
    displayName
      .split(" ")
      .map((part) => part[0])
      .join("")
      .slice(0, 2)
      .toUpperCase();

  return (

    <Sheet
      open={open}
      onOpenChange={
        onOpenChange
      }
    >

      <SheetContent
        side="left"
        className="w-[300px] p-0"
      >

        <SheetHeader
          className="
            border-b
            px-4
            py-4
            text-left
          "
        >

          <SheetTitle
            className="
              flex
              items-center
              gap-3
            "
          >

            <span
              className="
                grid
                size-9
                place-items-center
                rounded-lg
                bg-[#1E8E6A]
                text-white
              "
            >

              <GraduationCap
                className="size-5"
              />

            </span>

            <div>

              <span
                className="
                  block
                  text-sm
                  font-semibold
                "
              >
                Assistant TDE
              </span>

              <span
                className="
                  block
                  text-xs
                  text-muted-foreground
                "
              >
                {role}
              </span>

            </div>

          </SheetTitle>

        </SheetHeader>

        {/* Profil */}

        <div
          className="
            border-b
            p-4
          "
        >

          <div
            className="
              flex
              items-center
              gap-3
            "
          >

            <Avatar>

              <AvatarFallback>
                {initials}
              </AvatarFallback>

            </Avatar>

            <div>

              <p
                className="
                  text-sm
                  font-medium
                "
              >
                {displayName}
              </p>

              <p
                className="
                  text-xs
                  text-muted-foreground
                "
              >
                {user?.email}
              </p>

            </div>

          </div>

        </div>

        {/* Navigation */}

        <nav
          className="
            flex-1
            space-y-5
            overflow-y-auto
            px-3
            py-4
          "
        >

          {sections.map(
            (
              section,
              index
            ) => (

              <div
                key={index}
                className="
                  space-y-2
                "
              >

                {section.title && (

                  <p
                    className="
                      px-3
                      text-xs
                      font-medium
                      uppercase
                      tracking-wide
                      text-muted-foreground
                    "
                  >
                    {section.title}
                  </p>

                )}

                {section.items.map(
                  (item) => (

                    <SidebarButtonSheet
                      key={item.href}
                      item={item}
                    />

                  )
                )}

              </div>

            )
          )}

        </nav>

        {/* Déconnexion */}

        <div
          className="
            border-t
            p-3
          "
        >

          <button
            onClick={logout}
            className="
              flex
              w-full
              items-center
              gap-3
              rounded-xl
              px-3
              py-3
              text-red-600
              hover:bg-red-50
            "
          >

            <LogOut
              className="
                size-4
              "
            />

            Déconnexion

          </button>

        </div>

      </SheetContent>

    </Sheet>

  );

}