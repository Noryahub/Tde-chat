"use client";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Cell,
  Tooltip,
} from "recharts";

type IntentData = {
  intent: string;
  count: number;
};

type IntentChartProps = {
  data: IntentData[];
};

const COLORS = [
  "#2F80ED",
  "#9B51E0",
  "#F2994A",
  "#EB5757",
  "#56CCF2",
];

function CustomTooltip({
  active,
  payload,
  label,
  total,
}: {
  active?: boolean;
  payload?: { value: number }[];
  label?: string;
  total: number;
}) {
  if (!active || !payload?.length) return null;

  const count = Number(payload[0].value);
  const pct = total > 0
    ? Math.round((count / total) * 100)
    : 0;

  return (
    <div className="rounded-xl border border-gray-100 bg-white px-3 py-2 shadow-md">
      <p className="text-[13px] font-medium text-gray-800">
        {label}
      </p>

      <p className="text-[12px] text-gray-500">
        {count} conversations
      </p>

      <p className="text-[11px] text-gray-400">
        {pct}% du total
      </p>
    </div>
  );
}

export function IntentChart({
  data,
}: IntentChartProps) {

  const total = data.reduce(
    (sum, item) => sum + item.count,
    0
  );

  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm">

      <div className="mb-5 flex items-start justify-between">
        <div>
          <h3 className="text-[17px] font-medium text-gray-900">
            Répartition des besoins clients
          </h3>
        </div>

        <span className="flex items-center gap-1 rounded-lg bg-emerald-50 px-3 py-1 text-[11px] font-medium text-emerald-700">
          {data.length} catégories
        </span>
      </div>

      <ResponsiveContainer width="100%" height={240}>
        <BarChart
          data={data}
          margin={{
            top: 4,
            right: 4,
            left: -20,
            bottom: 0,
          }}
          barCategoryGap="10%"
        >
          <XAxis
            dataKey="intent"
            axisLine={false}
            tickLine={false}
            tick={{
              fontSize: 12,
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
          />

          <Tooltip
            content={
              <CustomTooltip
                total={total}
              />
            }
          />

          <Bar
            dataKey="count"
            radius={[8, 8, 8, 8]}
            barSize={28}
          >
            {data.map((entry, index) => (
              <Cell
                key={entry.intent}
                fill={
                  COLORS[
                    index % COLORS.length
                  ]
                }
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      <div className="mt-4 flex flex-wrap gap-3">
        {data.map((item, index) => (
          <div
            key={item.intent}
            className="flex items-center gap-1.5"
          >
            <span
              className="h-2 w-2 rounded-full"
              style={{
                background:
                  COLORS[
                    index % COLORS.length
                  ],
              }}
            />

            <span className="text-[12px] text-gray-500">
              {item.intent.replaceAll("_", " ")}
              {" "}
              <span className="text-gray-400">
                {Math.round(
                  (item.count / total) * 100
                )}
                %
              </span>
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}