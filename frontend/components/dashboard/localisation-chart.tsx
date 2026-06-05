"use client";

import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";

const data = [
  { name: "Lomé", value: 45 },
  { name: "Kara", value: 20 },
  { name: "Sokodé", value: 15 },
  { name: "Atakpamé", value: 10 },
  { name: "Dapaong", value: 10 },
];

const COLORS = [
  "#1D9E75",
  "#2F80ED",
  "#F2994A",
  "#EB5757",
  "#9B51E0",
];

export function LocalisationChart() {
  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
      <h3 className="mb-4 text-sm font-semibold text-[#111827]">
        Zones les plus touchées
      </h3>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            outerRadius={100}
            label
          >
            {data.map((entry, index) => (
              <Cell
                key={entry.name}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>

          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}