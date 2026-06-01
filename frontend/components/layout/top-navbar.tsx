"use client";

import { Menu, Bot } from "lucide-react";

type TopNavbarProps = {
  onMenuClick?: () => void;
};

export function TopNavbar({
  onMenuClick,
}: TopNavbarProps) {

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
        h-[78px]
        items-center
        justify-between
        border-b
        border-[#e8ecef]
        bg-white/95
        px-4
        backdrop-blur
        md:px-6
      "
    >

      {/* ====================================== */}
      {/* LEFT */}
      {/* ====================================== */}

      <div className="flex items-center gap-3">

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

        {/* BOT ICON */}

        <div
          className="
            flex
            h-12
            w-12
            shrink-0
            items-center
            justify-center
            rounded-full
            bg-[#e8f7f1]
            text-[#1D9E75]
          "
        >

          <Bot className="h-5 w-5" />

        </div>

        {/* TEXT */}

        <div className="leading-tight">

          <h1
            className="
              text-[14px]
              font-semibold
              text-[#111827]
            "
          >
            votre assistant
          </h1>

          <div
            className="
              mt-1
              flex
              items-center
              gap-1.5
            "
          >

            <span
              className="
                h-2
                w-2
                rounded-full
                bg-[#1D9E75]
              "
            />

            <p
              className="
                text-[13px]
                font-medium
                text-[#1D9E75]
              "
            >
              En ligne
            </p>

          </div>

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
          border-[#dfe5ea]
          bg-white
          shadow-sm
          transition-all
          duration-200
          hover:scale-105
        "
      >

        <img
          src={`https://ui-avatars.com/api/?name=${user.nom}&background=1D9E75&color=ffffff`}
          alt="avatar utilisateur"
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