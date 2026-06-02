import { post } from "@/services/api";
import type { ApiResponse } from "@/types";

type ChatResponse = ApiResponse<{
  response: string;
}>;

export async function sendMessage(
  message: string,
  session_id: string
) {
  const response = await post<ChatResponse>(
    "/chat/",
    {
      message,
      session_id,
    }
  );

  return response.response;
}