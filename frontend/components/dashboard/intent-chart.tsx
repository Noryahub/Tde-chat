"use client";

import { useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Cell,
  Tooltip,
} from "recharts";

const data = [
  { intent: "Facturation", count: 320 },
  { intent: "Coupure", count: 280 },
  { intent: "Branchement", count: 190 },
  { intent: "Fuite", count: 140 },
  { intent: "Réclamation", count: 90 },
];

const COLORS =  ["#2F80ED", "#9B51E0", "#F2994A", "#EB5757", "#56CCF2"];

const total = data.reduce((sum, d) => sum + d.count, 0);

function CustomTooltip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: { value: number; payload: { intent: string } }[];
  label?: string;
}) {
  if (!active || !payload?.length) return null;
  const count = payload[0].value;
  const pct = Math.round((count / total) * 100);

  return (
    <div className="rounded-xl border border-gray-100 bg-white px-3 py-2 shadow-md">
      <p className="text-[13px] font-medium text-gray-800">{label}</p>
      <p className="text-[12px] text-gray-500">
        {count} messages
      </p>
      <p className="text-[11px] text-gray-400">{pct}% du corpus</p>
    </div>
  );
}

export function IntentChart() {
  const dominant = data.reduce((a, b) => (a.count > b.count ? a : b));
  const minority = data.reduce((a, b) => (a.count < b.count ? a : b));

  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">

      {/* Header */}
      <div className="mb-5 flex items-start justify-between">
        <div>
          <h3 className="text-[17px] font-medium text-gray-900">
            Répartition des besoins clients
          </h3>
        </div>
        <span className="flex items-center gap-1 rounded-lg bg-emerald-50 px-3 py-1 text-[11px] font-medium text-emerald-700">
          {/* bar-chart icon (inline svg, no dependency) */}
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <rect x="3" y="12" width="4" height="9" /><rect x="10" y="7" width="4" height="14" /><rect x="17" y="3" width="4" height="18" />
          </svg>
          5 catégories
        </span>
      </div>


      {/* Chart */}
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
          <XAxis
            dataKey="intent"
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 12, fill: "#9CA3AF" }}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 11, fill: "#9CA3AF" }}
            tickCount={5}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: "rgba(0,0,0,0.04)" }} />
          <Bar dataKey="count" radius={[8, 8, 8, 8]} barSize={36}>
            {data.map((entry, index) => (
              <Cell key={entry.intent} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      {/* Legend */}
      <div className="mt-4 flex flex-wrap gap-3">
        {data.map((d, i) => (
          <div key={d.intent} className="flex items-center gap-1.5">
            <span
              className="h-2 w-2 flex-shrink-0 rounded-full"
              style={{ background: COLORS[i] }}
            />
            <span className="text-[12px] text-gray-500">
              {d.intent}{" "}
              <span className="text-gray-400">
                {Math.round((d.count / total) * 100)}%
              </span>
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}