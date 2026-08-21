import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";

export type UserRole = "admin" | "user";

export type AuthUser = {
  id: string | number;
  name?: string;
  nom?: string;
  email: string;
  role: UserRole;
};

export type AuthSession = {
  user: AuthUser;
  token: string;
};

export type SidebarItem = {
  title: string;
  href: string;
  icon: LucideIcon;
  badge?: string;
};

export type SidebarSection = {
  title?: string;
  items: SidebarItem[];
};

export type SidebarConfig = {
  role: UserRole;
  sections: SidebarSection[];
  footer?: ReactNode;
};

export type ApiResponse<T> = {
  status: "success" | "error";
  error?: string;
  message?: string;
} & T;

export type LoginPayload = {
  email: string;
  password: string;
};

export type RegisterPayload = {
  nom: string;
  email: string;
  password: string;
};

export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  conversationId?: number;
  content: string;
  createdAt: string;
};

export type Ticket = {
  id: number;
  user_id: number;
  ticket_number: string;
  nom: string | null;
  email: string | null;
  telephone: string;
  localisation: string;
  description: string;
  intent: string | null;
  statut: "ouvert" | "en_cours" | "resolu" | "cloture";
  created_at: string;
  updated_at: string;
};

export type History = {
  message_id: number;
  conversation_id: number;
  user_id: number;
  role: "user" | "assistant";
  content: string;
  created_at: string;
};

export type Conversation = {
  conversationId: number;
  title: string;
  createdAt: string;
  messages: ChatMessage[];
};

export type AnonymousQuota = {
  messages_used: number;
  messages_limit: number;
  messages_remaining: number;
};
