const API_URL = "http://127.0.0.1:5000";

type RequestOptions = {
  method?: string;
  body?: BodyInit | null;
  headers?: HeadersInit;
};

async function request<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {

  try {

    console.log(
      "FETCH URL :",
      `${API_URL}${endpoint}`
    );

    console.log(
      "FETCH BODY :",
      options.body
    );

    const response = await fetch(
      `${API_URL}${endpoint}`,
      {
        method: options.method || "GET",

        mode: "cors",

        headers: {
          "Content-Type": "application/json",
          ...(options.headers || {}),
        },

        body: options.body,
      }
    );

    console.log(
      "STATUS :",
      response.status
    );

    if (!response.ok) {
      throw new Error(
        `HTTP error ${response.status}`
      );
    }

    return response.json();

  } catch (error) {

    console.error(
      "FETCH ERROR :",
      error
    );

    throw error;
  }
}

export function get<T>(endpoint: string) {
  return request<T>(endpoint);
}

export function post<T>(
  endpoint: string,
  body?: BodyInit
) {
  return request<T>(endpoint, {
    method: "POST",
    body,
  });
}

export function patch<T>(
  endpoint: string,
  body?: BodyInit
) {
  return request<T>(endpoint, {
    method: "PATCH",
    body,
  });
}

export function del<T>(endpoint: string) {
  return request<T>(endpoint, {
    method: "DELETE",
  });
}