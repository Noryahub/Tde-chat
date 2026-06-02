const API_URL = "http://127.0.0.1:5000";

type RequestOptions = {
  method?: string;
  body?: unknown;
  headers?: HeadersInit;
};

function getToken(): string | null {

  if (typeof window === "undefined") {
    return null;
  }

  const session =
    localStorage.getItem(
      "assistant-tde-session"
    );

  if (!session) {
    return null;
  }

  try {

    const parsed =
      JSON.parse(session);

    return parsed.token || null;

  } catch {

    return null;

  }
}

async function request<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {

  const token = getToken();

  let body: string | undefined;

  if (options.body !== undefined) {

    body =
      typeof options.body === "string"
        ? options.body
        : JSON.stringify(
            options.body
          );
  }

  const response = await fetch(
    `${API_URL}${endpoint}`,
    {
      method:
        options.method || "GET",

      mode: "cors",

      headers: {
        "Content-Type":
          "application/json",

        ...(token
          ? {
              Authorization:
                `Bearer ${token}`,
            }
          : {}),

        ...(options.headers || {}),
      },

      body,
    }
  );

  if (!response.ok) {

    let errorMessage =
      `HTTP ${response.status}`;

    try {

      const error =
        await response.json();

      errorMessage =
        error.message ||
        errorMessage;

    } catch {}

    throw new Error(
      errorMessage
    );
  }

  return response.json();
}

export function get<T>(
  endpoint: string
) {
  return request<T>(endpoint);
}

export function post<T>(
  endpoint: string,
  body?: unknown
) {
  return request<T>(
    endpoint,
    {
      method: "POST",
      body,
    }
  );
}

export function patch<T>(
  endpoint: string,
  body?: unknown
) {
  return request<T>(
    endpoint,
    {
      method: "PATCH",
      body,
    }
  );
}

export function del<T>(
  endpoint: string
) {
  return request<T>(
    endpoint,
    {
      method: "DELETE",
    }
  );
}