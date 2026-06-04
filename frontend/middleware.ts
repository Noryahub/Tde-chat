import { NextResponse, type NextRequest } from "next/server";

const authRoutes = ["/login", "/register"];

export function middleware(request: NextRequest) {

  const { pathname } = request.nextUrl;

  const token =
    request.cookies.get(
      "assistant_tde_token"
    )?.value;

  const role =
    request.cookies.get(
      "assistant_tde_role"
    )?.value;

  const isAuthRoute =
    authRoutes.some((route) =>
      pathname.startsWith(route)
    );

  // Utilisateur déjà connecté
  if (isAuthRoute && token) {

    return NextResponse.redirect(
      new URL(
        role === "admin"
          ? "/admin/dashboard"
          : "/user/chat",
        request.url
      )
    );

  }

  // Protection ADMIN
  if (
    pathname.startsWith("/admin") &&
    !token
  ) {

    return NextResponse.redirect(
      new URL("/login", request.url)
    );

  }

  // Protection USER
  // ⚠️ sauf /user/chat qui reste public
  if (
    pathname.startsWith("/user") &&
    pathname !== "/user/chat" &&
    !token
  ) {

    return NextResponse.redirect(
      new URL("/login", request.url)
    );

  }

  // Empêcher un user normal
  // d'accéder à l'admin
  if (
    pathname.startsWith("/admin") &&
    role !== "admin"
  ) {

    return NextResponse.redirect(
      new URL("/user/chat", request.url)
    );

  }

  // Empêcher un admin
  // d'aller dans l'espace user
  if (
    pathname.startsWith("/user") &&
    pathname !== "/user/chat" &&
    role === "admin"
  ) {

    return NextResponse.redirect(
      new URL("/admin/dashboard", request.url)
    );

  }

  return NextResponse.next();

}

export const config = {
  matcher: [
    "/login",
    "/register",
    "/admin/:path*",
    "/user/:path*",
  ],
};