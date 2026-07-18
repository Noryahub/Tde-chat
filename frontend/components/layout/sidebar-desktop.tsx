"use client";

import { useState } from "react";
import { usePathname, useRouter } from "next/navigation";

import { useEffect } from "react";
import { loadConversations } from "@/storage/chat-storage";
import type { Conversation } from "@/types";

import { useChat } from "@/context/ChatContext";
import {
  ChevronLeft,
  ChevronRight,
  LayoutDashboard,
  MessageSquare,
  History,
  Settings,
  LogOut,
} from "lucide-react";

import { cn } from "@/lib/utils";
import { useAuth } from "@/hooks/use-auth";

import type {
    Conversation,
  SidebarSection,
  UserRole,
} from "@/types";

type SidebarDesktopProps = {
    collapsed: boolean;
    onCollapsedChange: (collapsed: boolean) => void;
    role: UserRole;
    sections: SidebarSection[];
};

export function SidebarDesktop({
    collapsed,
    onCollapsedChange,
    role,
    sections,
}: SidebarDesktopProps) {
  const router = useRouter();
  const pathname = usePathname();

const {
    conversationId,
    setConversationId,
    selectedConversationId,
    setSelectedConversationId,
    conversations,
    setConversations,
    newConversation,
} = useChat();
  // ======================================
  // USER TEMPORAIRE
  // ======================================

 const {
  user,
  isAuthenticated,
  logout,
} = useAuth();

//initialisation de l etat des conversations
{/*const [
  conversations,
  setConversations,
] = useState<Conversation[]>([]);
//chargement de l'historique
        useEffect(() => {
          async function fetchHistory() {
            if (
              !isAuthenticated ||
              !user
            ) {
              setConversations([]);
              setLoadingHistory(false);
              return;
            }
            try {
              const history =
                await loadConversations(
                  Number(user.id)
                );
              setConversations(history);
            } catch (error) {
              console.error(
                "Erreur chargement historique",
                error
              );
            } finally {
              setLoadingHistory(false);
            }
          }
          fetchHistory();
        }, [
          isAuthenticated,
          user,
        ]);
    const [
  loadingHistory,
  setLoadingHistory,
] = useState(true);
*/}



  // ======================================
  // LOGOUT
  // ======================================

  function handleLogout() {
    logout();
    }
  return (
    <aside
      className={cn(
        `
        fixed
        left-0
        top-0
        z-50
        hidden
        h-screen
        border-r
        border-[#e5e7eb]
        bg-white
        transition-all
        duration-300
        lg:flex
        lg:flex-col
        shadow-sm
        `,
        collapsed
          ? "w-[88px]"
          : "w-[280px]"
      )}
    >

      {/* ====================================== */}
      {/* HEADER */}
      {/* ====================================== */}

      <div className="relative flex h-[82px] items-center border-b border-[#f1f1f1] px-5">
        <div className="flex items-center gap-3 overflow-hidden">
          <div
            className="
              flex
              h-11
              w-11
              shrink-0
              items-center
              justify-center
              rounded-2xl
              bg-[#1E8E6A]
              text-white
              shadow-sm
              text-lg
            "
          >
          </div>
          {!collapsed && (
            <div className="min-w-0">
              <h1 className="truncate text-[15px] font-semibold text-[#111827]">
                Assistant TDE
              </h1>
              <p className="truncate text-xs text-[#6b7280]">
                Société Togolaise des Eaux
              </p>
            </div>
          )}
        </div>
        {/* ====================================== */}
        {/* TOGGLE */}
        {/* ====================================== */}
        <button
          onClick={() =>
            onCollapsedChange(!collapsed)
          }
          className="
            absolute
            -right-4
            top-1/2
            flex
            h-9
            w-9
            -translate-y-1/2
            items-center
            justify-center
            rounded-full
            border
            border-[#e5e7eb]
            bg-white
            shadow-md
            transition-all
            hover:scale-105
            hover:bg-[#f9fafb]
          "
        >
          {collapsed ? (
            <ChevronRight className="h-4 w-4 text-[#374151]" />
          ) : (
            <ChevronLeft className="h-4 w-4 text-[#374151]" />
          )}
        </button>
      </div>
      {/* ====================================== */}
      {/* NAVIGATION */}
      {/* ====================================== */}
      <div className="flex flex-1 flex-col overflow-hidden px-4 py-6">
    {/* ================= Navigation ================= */}
    <div className="space-y-2 shrink-0">
        {sections.map((section, index) => (
            <div
                key={index}
                className="space-y-2"
            >
                {section.items.map((item) => {
                    const Icon = item.icon;
                    const active =
                        pathname === item.href;
                    return (
                        <button
                            key={item.href}
                            onClick={() => {
                                 if (item.title === "Nouvelle conversation") {
                                    newConversation();
                                    return;
                                }
                                router.push(item.href)
                                }}
                            className={cn(
                                `
                                flex
                                w-full
                                items-center
                                gap-3
                                rounded-2xl
                                px-4
                                py-3
                                text-sm
                                font-medium
                                transition-all
                                duration-200
                                `,
                                active
                                    ? "bg-[#1E8E6A] text-white shadow-sm"
                                    : "text-[#374151] hover:bg-[#f3f4f6]"
                            )}
                        >
                            <Icon
                                className={cn(
                                    "h-5 w-5 shrink-0",
                                    active
                                        ? "text-white"
                                        : "text-[#6b7280]"
                                )}
                            />
                            {!collapsed && (
                                <span>{item.title}</span>
                            )}
                        </button>
                    );
                })}
            </div>
        ))}
    </div>
    {/* ================= Historique ================= */}
    {isAuthenticated && !collapsed && (
        <div className="mt-8 flex min-h-0 flex-1 flex-col">
            <div
                className="
                    min-h-0
                    flex-1
                    overflow-y-auto
                    pr-1
                    space-y-2
                    [scrollbar-width:thin]
                    [&::-webkit-scrollbar]:w-1.5
                    [&::-webkit-scrollbar-thumb]:rounded-full
                    [&::-webkit-scrollbar-thumb]:bg-gray-300
                "
            >
                   {conversations.length === 0 ? (
                            <p className="px-2 text-xs text-gray-400">
                                Aucun historique
                            </p>
                        )  : (
                    conversations.map((conversation) => (
                        <button
                            key={conversation.conversationId}
                            onClick={() => {
                            setSelectedConversationId(
                                conversation.conversationId
                            );
                            setConversationId(
                                conversation.conversationId
                            );
                        }}
                            className="
                                w-full
                                rounded-xl
                                px-3
                                py-2
                                text-left
                                hover:bg-gray-100
                            "
                        >
                            <div className="truncate font-medium">
                                {conversation.title}
                            </div>

                            <div className="text-xs text-gray-400">
                                {new Date(
                                    conversation.createdAt
                                ).toLocaleDateString("fr-FR")}
                            </div>
                        </button>
                    ))
                )}
            </div>
        </div>
    )}
</div>
{/* FOOTER */}
{isAuthenticated && (
  <div className="border-t border-[#f1f1f1] p-4">
    <div
      className={cn(
        `
        mb-4
        flex
        items-center
        gap-3
        rounded-2xl
        border
        border-[#f1f1f1]
        bg-[#fafafa]
        p-3
        transition-all
        `,
        collapsed && "justify-center"
      )}
    >
      <img
        src={`https://ui-avatars.com/api/?name=${user?.nom || "User"}&background=1E8E6A&color=fff`}
        alt="avatar"
        className="
          h-4
          w-4
          rounded-full
          object-cover
          shadow-sm
        "
      />
      {!collapsed && (
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold text-[#111827]">
            {user?.name}
          </p>
          <p className="truncate text-sm text-[#6b7280]">
            {user?.email}
          </p>
        </div>
      )}
    </div>
    <button
      onClick={handleLogout}
      className="
        flex
        w-full
        items-center
        gap-3
        rounded-2xl
        px-4
        py-3
        text-sm
        font-medium
        text-[#dc2626]
        transition-colors
        hover:bg-red-50
      "
    >
      <LogOut className="h-3 w-3 shrink-0" />
      {!collapsed && (
        <span>Déconnexion</span>
      )}
    </button>
  </div>
)}
</aside>
);
}