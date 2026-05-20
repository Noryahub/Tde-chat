export default function UserHistoryPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Historique</h1>
        <p className="mt-1 text-sm text-muted-foreground">Vos conversations recentes avec l'assistant.</p>
      </div>
      <div className="space-y-3">
        {["Orientation licence", "Procedure d'inscription", "Documents requis"].map((title) => (
          <article key={title} className="rounded-lg border bg-card p-4">
            <h2 className="font-medium">{title}</h2>
            <p className="mt-2 text-sm text-muted-foreground">Dernier echange conserve dans votre espace.</p>
          </article>
        ))}
      </div>
    </div>
  );
}
