export default function AdminAnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Analytics</h1>
        <p className="mt-1 text-sm text-muted-foreground">Qualite des reponses et tendances d'usage.</p>
      </div>
      <div className="grid gap-4 lg:grid-cols-[2fr_1fr]">
        <section className="rounded-lg border bg-card p-5">
          <h2 className="text-base font-semibold">Volume de conversations</h2>
          <div className="mt-6 flex h-64 items-end gap-3">
            {[42, 64, 48, 80, 76, 92, 70].map((height, index) => (
              <div key={index} className="flex flex-1 flex-col items-center gap-2">
                <div className="w-full rounded-t-md bg-foreground" style={{ height: `${height}%` }} />
                <span className="text-xs text-muted-foreground">J{index + 1}</span>
              </div>
            ))}
          </div>
        </section>
        <section className="rounded-lg border bg-card p-5">
          <h2 className="text-base font-semibold">Indicateurs</h2>
          <div className="mt-4 space-y-4 text-sm">
            <p className="flex justify-between"><span>Taux de resolution</span><strong>86%</strong></p>
            <p className="flex justify-between"><span>Temps moyen</span><strong>1m 42s</strong></p>
            <p className="flex justify-between"><span>Satisfaction</span><strong>4.6/5</strong></p>
          </div>
        </section>
      </div>
    </div>
  );
}
