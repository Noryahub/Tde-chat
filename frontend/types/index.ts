import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";

export type UserRole = "admin" | "user";

export type AuthUser = {
  id: string;
  name: string;
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
  content: string;
  createdAt: string;
};

export type Ticket = {
  id: number;
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