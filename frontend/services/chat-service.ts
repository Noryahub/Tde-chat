import { post } from "@/services/api";
import type { ApiResponse } from "@/types";

type ChatResponse = ApiResponse<{
  response: string;
}>;

export async function sendMessage(
  message: string,
  session_id: string,
  user_id: string
) {

  const response = await post<ChatResponse>(
    "/chat/",
    JSON.stringify({
      message,
      session_id,
      user_id,
    })
  );

  return response.response;
}