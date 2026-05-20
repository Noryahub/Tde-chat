const users = [
  { name: "Amina Diallo", email: "amina@example.com", role: "user", status: "Actif" },
  { name: "Karim Benali", email: "karim@example.com", role: "admin", status: "Actif" },
  { name: "Sofia Martin", email: "sofia@example.com", role: "user", status: "Invite" },
];

export default function AdminUsersPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Utilisateurs</h1>
        <p className="mt-1 text-sm text-muted-foreground">Gestion des comptes et roles.</p>
      </div>
      <section className="overflow-hidden rounded-lg border bg-card">
        <div className="grid grid-cols-4 border-b px-4 py-3 text-xs font-medium uppercase text-muted-foreground">
          <span>Nom</span><span>Email</span><span>Role</span><span>Statut</span>
        </div>
        {users.map((user) => (
          <div key={user.email} className="grid grid-cols-4 px-4 py-4 text-sm">
            <span className="font-medium">{user.name}</span>
            <span className="text-muted-foreground">{user.email}</span>
            <span className="capitalize">{user.role}</span>
            <span>{user.status}</span>
          </div>
        ))}
      </section>
    </div>
  );
}
