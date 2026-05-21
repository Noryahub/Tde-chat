"use client";

import { Menu } from "lucide-react";

import { usePathname } from "next/navigation";

const titles: Record<string, string> = {
  "/admin/dashboard": "Dashboard admin",
  "/admin/analytics": "Analytics",
  "/admin/users": "Utilisateurs",
  "/admin/signalements": "Signalements",
  "/admin/settings": "Paramètres",

  "/user/chat": "Chat TDE",
  "/user/history": "Historique",
  "/user/profile": "Profil",
  "/user/settings": "Paramètres",
};

type TopNavbarProps = {
  onMenuClick?: () => void;
};

export function TopNavbar({
  onMenuClick,
}: TopNavbarProps) {

  const pathname = usePathname();

  const user = {
    nom: "Betsalel",
  };

  return (

    <header
      className="
        sticky
        top-0
        z-30
        flex
        h-[72px]
        items-center
        justify-between
        border-b
        border-[#ececec]
        bg-white
        px-5
        lg:px-8
      "
    >

      {/* ====================================== */}
      {/* LEFT */}
      {/* ====================================== */}

      <div className="flex items-center gap-4">

        {/* MOBILE BUTTON */}

        <button
          onClick={onMenuClick}
          className="
            flex
            h-10
            w-10
            items-center
            justify-center
            rounded-xl
            border
            border-[#ececec]
            bg-white
            transition-colors
            hover:bg-[#f5f5f5]
            lg:hidden
          "
        >

          <Menu className="h-5 w-5 text-[#374151]" />

        </button>

        {/* TITLE */}

        <div>

          <h1
            className="
              text-[18px]
              font-semibold
              text-[#111827]
            "
          >

          </h1>

          <p
            className="
              text-sm
              text-[#6b7280]
            "
          >
            Connecté en tant qu'utilisateur
          </p>

        </div>

      </div>

      {/* ====================================== */}
      {/* USER AVATAR */}
      {/* ====================================== */}

      <button
        className="
          flex
          h-11
          w-11
          items-center
          justify-center
          overflow-hidden
          rounded-full
          border
          border-[#e5e7eb]
          bg-[#f9fafb]
          transition-all
          hover:scale-105
        "
      >

        <img
          src={`https://ui-avatars.com/api/?name=${user.nom}&background=1E8E6A&color=fff`}
          alt="avatar"
          className="
            h-full
            w-full
            object-cover
          "
        />

      </button>

    </header>
  );
}