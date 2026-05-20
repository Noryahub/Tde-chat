import { Activity, MessageSquareText, ShieldAlert, UsersRound } from "lucide-react";

const stats = [
  { label: "Utilisateurs", value: "1 248", icon: UsersRound },
  { label: "Conversations", value: "8 392", icon: MessageSquareText },
  { label: "Signalements", value: "12", icon: ShieldAlert },
  { label: "Disponibilite", value: "99.8%", icon: Activity },
];

export default function AdminDashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Vue d'ensemble</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Supervision des usages, utilisateurs et signalements.
        </p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <article key={stat.label} className="rounded-lg border bg-card p-4">
            <div className="flex items-center justify-between">
              <p className="text-sm text-muted-foreground">{stat.label}</p>
              <stat.icon className="size-4 text-muted-foreground" />
            </div>
            <p className="mt-4 text-2xl font-semibold">{stat.value}</p>
          </article>
        ))}
      </div>
      <section className="rounded-lg border bg-card p-5">
        <h2 className="text-base font-semibold">Activite recente</h2>
        <div className="mt-4 space-y-3">
          {["Nouvel utilisateur inscrit", "Conversation resolue", "Signalement en attente"].map((item) => (
            <div key={item} className="flex items-center justify-between rounded-lg border bg-background px-3 py-2 text-sm">
              <span>{item}</span>
              <span className="text-muted-foreground">Aujourd'hui</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
