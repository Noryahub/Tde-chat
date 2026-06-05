const API_URL = "http://127.0.0.1:5000/api/admin";

export async function getDashboardAnalytics() {
  const response = await fetch(
    `${API_URL}/dashboard`
  );

  if (!response.ok) {
    throw new Error("Erreur chargement dashboard");
  }

  const data = await response.json();

  return data.data;
}

export async function getLatestSignalements() {
  const response = await fetch(
    `${API_URL}/signalements`
  );

  if (!response.ok) {
    throw new Error("Erreur chargement signalements");
  }

  const data = await response.json();

  return data.data;
}