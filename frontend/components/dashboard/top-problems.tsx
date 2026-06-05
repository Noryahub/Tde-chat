"use client";

interface ProblemData {
  probleme: string;
  count: number;
}

interface TopProblemsProps {
  data: ProblemData[];
}

const BAR_COLOR = "#1D9E75";

export function TopProblems({
  data,
}: TopProblemsProps) {

  const total = data.reduce(
    (sum, d) => sum + d.count,
    0
  );

  const max =
    data.length > 0
      ? Math.max(
          ...data.map((d) => d.count)
        )
      : 0;

  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm">

      {/* Header */}
      <div className="mb-5">
        <p className="mb-1 text-[11px] font-medium uppercase tracking-widest text-gray-400">
          Problèmes les plus fréquents
        </p>
      </div>

      {data.length === 0 ? (
        <div className="py-6 text-center text-sm text-gray-400">
          Aucun problème détecté
        </div>
      ) : (
        <div className="space-y-4">
          {data.map((row) => {

            const pct =
              total > 0
                ? Math.round(
                    (row.count / total) * 100
                  )
                : 0;

            const barWidth =
              max > 0
                ? Math.round(
                    (row.count / max) * 100
                  )
                : 0;

            return (
              <div key={row.probleme}>

                <div className="mb-1.5 flex items-center justify-between">

                  <div className="flex items-center gap-2">
                    <span className="text-[13px] text-gray-500">
                      {row.probleme}
                    </span>
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

                <div className="h-4 w-full overflow-hidden rounded-full bg-gray-100">
                  <div
                    className="h-full rounded-full transition-all duration-500"
                    style={{
                      width: `${barWidth}%`,
                      background: BAR_COLOR,
                    }}
                  />
                </div>

              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}