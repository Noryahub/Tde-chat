export default function AdminSignalementsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Signalements</h1>
        <p className="mt-1 text-sm text-muted-foreground">Suivi des reponses a verifier.</p>
      </div>
      <div className="space-y-3">
        {["Reponse incomplete", "Question hors perimetre", "Feedback negatif"].map((item) => (
          <article key={item} className="rounded-lg border bg-card p-4">
            <div className="flex items-center justify-between gap-4">
              <h2 className="font-medium">{item}</h2>
              <span className="rounded-full bg-muted px-2 py-1 text-xs text-muted-foreground">A traiter</span>
            </div>
            <p className="mt-2 text-sm text-muted-foreground">Conversation marquee pour revue administrateur.</p>
          </article>
        ))}
      </div>
    </div>
  );
}
