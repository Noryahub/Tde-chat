import { RegisterForm } from "@/components/auth/register-form";

export default function RegisterPage() {
  return (
    <main className="grid min-h-screen bg-[radial-gradient(circle_at_top_left,var(--muted),transparent_32rem)] px-4 py-10">
      <section className="m-auto w-full max-w-md rounded-lg border bg-card p-6 shadow-sm">
        <div className="mb-6">
          <p className="text-sm font-medium text-muted-foreground">Assistant TDE</p>
          <h1 className="mt-2 text-2xl font-semibold tracking-tight">Creation de compte</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Creez un compte pour utiliser l'assistant.
          </p>
        </div>
        <RegisterForm />
      </section>
    </main>
  );
}
