"use client";

type Signalement = {
  localisation: string;
  probleme: string;
  statut: string;
  created_at: string;
};

interface LatestReportsProps {
  data: Signalement[];
}

const STATUT_CONFIG = {
  nouveau: {
    label: "Nouveau",
    bg: "bg-amber-50",
    text: "text-amber-700",
    dot: "bg-amber-400",
  },
  en_cours: {
    label: "En cours",
    bg: "bg-blue-50",
    text: "text-blue-700",
    dot: "bg-blue-400",
  },
  resolu: {
    label: "Résolu",
    bg: "bg-gray-100",
    text: "text-gray-500",
    dot: "bg-gray-400",
  },
};

function StatutBadge({
  statut,
}: {
  statut: string;
}) {
  const cfg =
    STATUT_CONFIG[
      statut as keyof typeof STATUT_CONFIG
    ] || STATUT_CONFIG.nouveau;

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-md px-2 py-0.5 text-[11px] font-medium ${cfg.bg} ${cfg.text}`}
    >
      <span
        className={`h-1.5 w-1.5 rounded-full ${cfg.dot}`}
      />
      {cfg.label}
    </span>
  );
}

export function LatestReports({
  data,
}: LatestReportsProps) {

  const newCount = data.filter(
    (item) => item.statut === "nouveau"
  ).length;

  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm">

      <div className="mb-5 flex items-start justify-between">
        <div>
          <p className="mb-1 text-[11px] font-medium uppercase tracking-widest text-gray-400">
            Remontées terrain — Temps réel
          </p>

          <h3 className="text-[17px] font-medium text-gray-900">
            Derniers signalements
          </h3>
        </div>

        {newCount > 0 && (
          <span className="flex items-center gap-1.5 rounded-lg bg-amber-50 px-3 py-1 text-[11px] font-medium text-amber-700">
            <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
            {newCount} nouveau{newCount > 1 ? "x" : ""}
          </span>
        )}
      </div>

      <div className="max-h-[320px] overflow-y-auto divide-y divide-gray-50 pr-1">
        {data.map((s, index) => (
          <div
            key={index}
            className="flex items-center gap-3 py-3"
          >
            <div className="min-w-0 flex-1">
              <p className="truncate text-[13px] font-medium text-gray-800">
                {s.localisation || "Non renseigné"}
              </p>

              <p className="truncate text-[12px] text-gray-400">
                {s.probleme || "Non renseigné"}
              </p>
            </div>

            <div className="flex flex-shrink-0 flex-col items-end gap-1">
              <StatutBadge statut={s.statut} />

              <span className="text-[11px] text-gray-400">
                {new Date(
                  s.created_at
                ).toLocaleDateString("fr-FR")}
              </span>
            </div>
          </div>
        ))}

        {data.length === 0 && (
          <div className="py-6 text-center text-sm text-gray-400">
            Aucun signalement trouvé
          </div>
        )}
      </div>
    </div>
  );
}