"use client";

type Statut = "nouveau" | "en_cours" | "resolu";

interface Signalement {
  id: number;
  localisation: string;
  probleme: string;
  created_at: string;
  statut: Statut;
}

const data: Signalement[] = [
  { id: 1, localisation: "Lomé - Bè",       probleme: "Coupure d'eau",         created_at: "2025-06-04 08:32", statut: "nouveau" },
  { id: 2, localisation: "Kara - Centre",    probleme: "Fuite sur réseau",      created_at: "2025-06-04 09:15", statut: "en_cours" },
  { id: 3, localisation: "Sokodé",           probleme: "Pression insuffisante", created_at: "2025-06-04 10:02", statut: "nouveau" },
  { id: 4, localisation: "Lomé - Adidogomé", probleme: "Facture incorrecte",    created_at: "2025-06-03 17:44", statut: "resolu" },
  { id: 5, localisation: "Atakpamé",         probleme: "Compteur défectueux",   created_at: "2025-06-03 15:20", statut: "en_cours" },
  { id: 6, localisation: "Tsévié",           probleme: "Branchement en attente",created_at: "2025-06-03 11:08", statut: "nouveau" },
  { id: 7, localisation: "Lomé - Agoè",     probleme: "Coupure d'eau",         created_at: "2025-06-02 09:55", statut: "resolu" },
  { id: 8, localisation: "Dapaong",          probleme: "Fuite sur réseau",      created_at: "2025-06-02 08:10", statut: "nouveau" },
];

const STATUT_CONFIG: Record<Statut, { label: string; bg: string; text: string; dot: string }> = {
  nouveau:  { label: "Nouveau",  bg: "bg-amber-50",  text: "text-amber-700",  dot: "bg-amber-400" },
  en_cours: { label: "En cours", bg: "bg-blue-50",   text: "text-blue-700",   dot: "bg-blue-400" },
  resolu:   { label: "Résolu",   bg: "bg-gray-100",  text: "text-gray-500",   dot: "bg-gray-400" },
};

function StatutBadge({ statut }: { statut: Statut }) {
  const cfg = STATUT_CONFIG[statut];
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-md px-2 py-0.5 text-[11px] font-medium ${cfg.bg} ${cfg.text}`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${cfg.dot}`} />
      {cfg.label}
    </span>
  );
}

export function LatestReports() {
  const newCount = data.filter((d) => d.statut === "nouveau").length;

  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">

      {/* Header */}
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

      {/* Table */}
      <div className="max-h-[320px] overflow-y-auto divide-y divide-gray-50 pr-1 scrollbar-thin scrollbar-thumb-gray-200 scrollbar-track-transparent">
        {data.map((s) => (
          <div key={s.id} className="flex items-center gap-3 py-3">

            {/* Left — location + problem */}
            <div className="min-w-0 flex-1">
              <p className="truncate text-[13px] font-medium text-gray-800">
                {s.localisation}
              </p>
              <p className="truncate text-[12px] text-gray-400">{s.probleme}</p>
            </div>

            {/* Right — date + badge */}
            <div className="flex flex-shrink-0 flex-col items-end gap-1">
              <StatutBadge statut={s.statut} />
              <span className="text-[11px] text-gray-400">{s.created_at}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}