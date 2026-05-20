export default function AdminSettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Parametres</h1>
        <p className="mt-1 text-sm text-muted-foreground">Configuration globale de l'application.</p>
      </div>
      <section className="rounded-lg border bg-card p-5">
        <h2 className="text-base font-semibold">Preferences systeme</h2>
        <div className="mt-5 space-y-4">
          {["Moderation active", "Historique conversations", "Mode sombre pret"].map((label) => (
            <label key={label} className="flex items-center justify-between rounded-lg border bg-background px-3 py-3 text-sm">
              <span>{label}</span>
              <input type="checkbox" defaultChecked className="size-4" />
            </label>
          ))}
        </div>
      </section>
    </div>
  );
}
