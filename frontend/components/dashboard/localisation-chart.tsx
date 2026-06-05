"use client";

import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";

interface LocalisationData {
  localisation: string;
  count: number;
}

interface LocalisationChartProps {
  data: LocalisationData[];
}

const COLORS = [
  "#1D9E75",
  "#2F80ED",
  "#F2994A",
  "#EB5757",
  "#9B51E0",
  "#56CCF2",
];

export function LocalisationChart({
  data,
}: LocalisationChartProps) {

  const chartData = data.map((item) => ({
    name: item.localisation,
    value: item.count,
  }));

  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm">

      <h3 className="mb-4 text-sm font-semibold text-[#111827]">
        Zones les plus touchées
      </h3>

      <ResponsiveContainer
        width="100%"
        height={300}
      >
        <PieChart>

          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            outerRadius={100}
            label
          >
            {chartData.map((entry, index) => (
              <Cell
                key={entry.name}
                fill={
                  COLORS[
                    index % COLORS.length
                  ]
                }
              />
            ))}
          </Pie>

          <Tooltip />

          <Legend />

        </PieChart>
      </ResponsiveContainer>

      {chartData.length === 0 && (
        <div className="py-4 text-center text-sm text-gray-400">
          Aucune donnée disponible
        </div>
      )}
    </div>
  );
}