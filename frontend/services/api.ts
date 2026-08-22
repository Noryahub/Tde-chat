const API_URL = "http://127.0.0.1:5000";

type RequestOptions = {
  method?: string;
  body?: unknown;
  headers?: HeadersInit;
};

export class ApiError extends Error {
  status: number;
  payload: unknown;
  code?: string;

  constructor(
    message: string,
    status: number,
    payload: unknown,
    code?: string
  ) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.payload = payload;
    this.code = code;
  }
}

export class AnonymousQuotaExceededError extends ApiError {
  constructor(
    payload: unknown
  ) {
    super(
      "Anonymous quota exceeded",
      429,
      payload,
      "anonymous_quota_exceeded"
    );
    this.name = "AnonymousQuotaExceededError";
  }
}

export function isAnonymousQuotaExceededError(
  error: unknown
): error is ApiError {
  return (
    error instanceof AnonymousQuotaExceededError ||
    (
      error instanceof ApiError &&
      error.status === 429 &&
      error.code === "anonymous_quota_exceeded"
    )
  );
}

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

      credentials: "include",

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
    let errorPayload: unknown = null;
    let errorCode: string | undefined;

    try {

      const error =
        await response.json();
      errorPayload = error;

      errorMessage =
        error.message ||
        errorMessage;
      errorCode = error.error;

    } catch {}

    if (
      response.status === 429 &&
      errorCode === "anonymous_quota_exceeded"
    ) {
      throw new AnonymousQuotaExceededError(
        errorPayload
      );
    }

    throw new ApiError(
      errorMessage,
      response.status,
      errorPayload,
      errorCode
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
