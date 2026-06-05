"use client";

import { ReactNode } from "react";

type StatsCardProps = {
  title: string;
  value: string | number;
  icon?: ReactNode;
};

export function StatsCard({
  title,
  value,
  icon,
}: StatsCardProps) {
  return (
    <div
      className="
        rounded-2xl
        border
        border-[#e5e7eb]
        bg-white
        p-5
        shadow-sm
      "
    >
      <div className="flex items-start justify-between">
        <div>
          <p
            className="
              text-sm
              text-[#6b7280]
            "
          >
            {title}
          </p>

          <h3
            className="
              mt-3
              text-xl
              font-bold
              text-gray-700
            "
          >
            {value}
          </h3>
        </div>

        {icon && (
          <div
            className="
              flex
              h-12
              w-12
              items-center
              justify-center
              rounded-xl
              bg-[#e8f7f1]
              text-[#1D9E75]
            "
          >
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}