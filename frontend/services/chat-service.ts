import { post } from "@/services/api";
import type { ApiResponse } from "@/types";

export type ChatData = {
  response: string;
  intent: string;
  ticket_proposal: boolean;
  conversation_id: number;
};
type ChatResponse = ApiResponse<ChatData>;

export async function sendMessage(
  message: string,
  session_id: string,
  conversation_id: number | null
) {
  const response = await post<ChatResponse>(
    "/chat/",
    {
      message,
      session_id,
      conversation_id,
    }
  );
  console.log("API RESPONSE", response);
  return response;
}