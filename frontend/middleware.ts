import { NextResponse, type NextRequest } from "next/server";

const authRoutes = ["/login", "/register"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get("assistant_tde_token")?.value;
  const role = request.cookies.get("assistant_tde_role")?.value;
  const isAuthRoute = authRoutes.some((route) => pathname.startsWith(route));

  if (isAuthRoute && token) {
    return NextResponse.redirect(
      new URL(role === "admin" ? "/admin/dashboard" : "/user/chat", request.url)
    );
  }

  if ((pathname.startsWith("/admin") || pathname.startsWith("/user")) && !token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (pathname.startsWith("/admin") && role !== "admin") {
    return NextResponse.redirect(new URL("/user/chat", request.url));
  }

  if (pathname.startsWith("/user") && role === "admin") {
    return NextResponse.redirect(new URL("/admin/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/login", "/register", "/admin/:path*", "/user/:path*"],
};
