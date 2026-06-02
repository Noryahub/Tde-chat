import { del, get, patch, post } from "@/services/api";

import type {
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
  return post("/auth/login", {
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
  return post("/auth/register", {
    nom: payload.nom,
    email: payload.email,
    password: payload.password,
  });
}

// =========================================
// CURRENT USER
// =========================================

export async function getCurrentUser() {
  return get("/auth/me");
}

// =========================================
// LOGOUT
// =========================================

export function logout() {
  localStorage.removeItem("token");
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
