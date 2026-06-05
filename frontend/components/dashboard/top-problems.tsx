"use client";

const data = [
  { probleme: "Coupure d'eau prolongée", count: 148 },
  { probleme: "Fuite sur réseau public", count: 112 },
  { probleme: "Facture incorrecte", count: 97 },
  { probleme: "Pression insuffisante", count: 73 },
  { probleme: "Branchement non effectué", count: 54 },
  { probleme: "Compteur défectueux", count: 38 },
];

const total = data.reduce((sum, d) => sum + d.count, 0);

const BAR_COLOR = "#1D9E75";

export function TopProblems() {
  const max = Math.max(...data.map((d) => d.count));

  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">

      {/* Header */}
      <div className="mb-5">
        <p className="mb-1 text-[11px] font-medium uppercase tracking-widest text-gray-400">
          Problèmes les plus fréquents
        </p>
      </div>

      {/* List */}
      <div className="space-y-4">
        {data.map((row, i) => {
          const pct = Math.round((row.count / total) * 100);
          const barWidth = Math.round((row.count / max) * 100);

          return (
            <div key={row.probleme}>
              {/* Label row */}
              <div className="mb-1.5 flex items-center justify-between">
                <div className="flex items-center gap-2">

                  <span className="text-[13px] text-gray-500">{row.probleme}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[13px] font-medium text-gray-800">
                    {row.count}
                  </span>
                  <span className="w-8 text-right text-[11px] text-gray-400">
                    {pct}%
                  </span>
                </div>
              </div>

              {/* Progress bar */}
              <div className="h-4 w-full overflow-hidden rounded-full bg-gray-100">
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{ width: `${barWidth}%`, background: BAR_COLOR }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}