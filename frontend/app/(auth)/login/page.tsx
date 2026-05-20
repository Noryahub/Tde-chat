import { LoginForm } from "@/components/auth/login-form";

export default function LoginPage() {
  return (
    <main className="grid min-h-screen bg-[radial-gradient(circle_at_top_left,var(--muted),transparent_32rem)] px-4 py-10">
      <section className="m-auto w-full max-w-md rounded-lg border bg-card p-6 shadow-sm">
        <div className="mb-6">
          <p className="text-sm font-medium text-muted-foreground">Assistant TDE</p>
          <h1 className="mt-2 text-2xl font-semibold tracking-tight">Connexion</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Accedez a votre espace admin ou utilisateur.
          </p>
        </div>
        <LoginForm />
      </section>
    </main>
  );
}
