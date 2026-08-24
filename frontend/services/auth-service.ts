import { del, get, patch, post } from "@/services/api";

import type {
  AuthSession,
  LoginPayload,
  RegisterPayload,
  User,
  UserRole,
} from "@/types";

// =========================================
// LOGIN
// =========================================

export async function login(
  payload: LoginPayload
) {
  return post<AuthSession>("/auth/login", {
    email: payload.email,
    password: payload.password,
  });
}

// =========================================
// REGISTER
// =========================================

export async function register(
  payload: RegisterPayload
) {
  return post<{ status: string; message: string; user_id: number }>(
    "/auth/register",
    {
    nom: payload.nom,
    email: payload.email,
    password: payload.password,
    }
  );
}

// =========================================
// CURRENT USER
// =========================================

export async function getCurrentUser() {
  return get<{
    status: string;
    user: User;
  }>("/auth/me");
}

// =========================================
// LOGOUT
// =========================================

export function logout() {
  localStorage.removeItem("token");
}

// =========================================
// GOOGLE OAUTH
// =========================================

const GOOGLE_OAUTH_BACKEND_URL = "http://localhost:5000";

export function startGoogleLogin(
  sessionId: string,
  redirectPath = "/user/chat"
): string {
  const params = new URLSearchParams({
    session_id: sessionId,
    redirect_path: redirectPath,
  });

  return `${GOOGLE_OAUTH_BACKEND_URL}/auth/google/start?${params.toString()}`;
}

export async function exchangeGoogleLogin(
  code: string
) {
  return post<
    AuthSession & {
      attached_conversations?: number;
    }
  >(
    "/auth/google/exchange",
    { code }
  );
}

// =========================================
// ADMIN — USERS
// =========================================

export async function getAllUsers() {
  return get<User[]>("/admin/users");
}

export async function updateRole(
  userId: number | string,
  role: UserRole
) {
  return patch(
    `/admin/users/${userId}/role`,
    { role }
  );
}

export async function deleteUser(
  userId: number | string
) {
  return del(
    `/admin/users/${userId}`
  );
}
