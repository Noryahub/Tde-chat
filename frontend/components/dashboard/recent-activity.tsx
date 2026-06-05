"use client";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

interface ActivityData {
  jour: string;
  count: number;
}

interface RecentActivityProps {
  data: ActivityData[];
}

function CustomTooltip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: { value: number }[];
  label?: string;
}) {
  if (!active || !payload?.length) return null;

  return (
    <div className="rounded-xl border border-gray-100 bg-white px-3 py-2 shadow-md">
      <p className="text-[12px] font-medium text-gray-800">
        {label}
      </p>

      <p className="text-[12px] text-gray-500">
        {payload[0].value} conversations
      </p>
    </div>
  );
}

export function RecentActivity({
  data,
}: RecentActivityProps) {

  const chartData = data.map((item) => ({
    jour: new Date(item.jour).toLocaleDateString(
      "fr-FR",
      {
        day: "2-digit",
        month: "short",
      }
    ),
    count: item.count,
  }));

  const max =
    chartData.length > 0
      ? Math.max(
          ...chartData.map((d) => d.count)
        )
      : 0;

  function CustomDot(props: any) {
    const { cx, cy, payload } = props;

    const isMax =
      payload.count === max;

    return (
      <circle
        cx={cx}
        cy={cy}
        r={isMax ? 5 : 3}
        fill={
          isMax
            ? "#2F80ED"
            : "#FFFFFF"
        }
        stroke="#2F80ED"
        strokeWidth={2}
      />
    );
  }

  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm">

      <div className="mb-5 flex items-start justify-between">
        <div>
          <p className="mb-1 text-[11px] font-medium uppercase tracking-widest text-gray-400">
            Activité des 7 derniers jours
          </p>
        </div>

        <span className="flex items-center gap-1 rounded-lg bg-blue-50 px-3 py-1 text-[11px] font-medium text-blue-700">
          <svg
            width="13"
            height="13"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
          </svg>

          7 jours
        </span>
      </div>

      <ResponsiveContainer
        width="100%"
        height={220}
      >
        <LineChart
          data={chartData}
          margin={{
            top: 8,
            right: 8,
            left: -20,
            bottom: 0,
          }}
        >
          <CartesianGrid
            strokeDasharray="4 4"
            stroke="rgba(0,0,0,0.05)"
            vertical={false}
          />

          <XAxis
            dataKey="jour"
            axisLine={false}
            tickLine={false}
            tick={{
              fontSize: 11,
              fill: "#9CA3AF",
            }}
          />

          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{
              fontSize: 11,
              fill: "#9CA3AF",
            }}
            tickCount={5}
          />

          <Tooltip
            content={<CustomTooltip />}
            cursor={{
              stroke:
                "rgba(0,0,0,0.06)",
              strokeWidth: 1,
            }}
          />

          <Line
            type="monotone"
            dataKey="count"
            stroke="#2F80ED"
            strokeWidth={2}
            dot={<CustomDot />}
            activeDot={{
              r: 5,
              fill: "#2F80ED",
              stroke: "#fff",
              strokeWidth: 2,
            }}
          />
        </LineChart>
      </ResponsiveContainer>

      {chartData.length === 0 && (
        <div className="py-6 text-center text-sm text-gray-400">
          Aucune activité disponible
        </div>
      )}
    </div>
  );
}