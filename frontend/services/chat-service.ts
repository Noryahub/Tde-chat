import {
  isAnonymousQuotaExceededError,
  post,
} from "@/services/api";
import type {
  AnonymousQuota,
  ApiResponse,
} from "@/types";

export type ChatData = {
  response: string;
  intent: string;
  ticket_proposal: boolean;
  conversation_id: number;
  quota?: AnonymousQuota;
};
type ChatResponse = ApiResponse<ChatData>;
type AnonymousQuotaExceededResponse = {
  status: "quota_exceeded";
  error: "anonymous_quota_exceeded";
  messages_remaining: number;
  messages_limit: number;
};

export type SendMessageResponse =
  | ChatResponse
  | AnonymousQuotaExceededResponse;

function readQuotaPayload(
  payload: unknown
) {
  if (
    payload &&
    typeof payload === "object" &&
    "messages_remaining" in payload &&
    "messages_limit" in payload
  ) {
    return payload as {
      messages_remaining: number;
      messages_limit: number;
    };
  }

  return {
    messages_remaining: 0,
    messages_limit: 5,
  };
}

export async function sendMessage(
  message: string,
  session_id: string,
  conversation_id: number | null
): Promise<SendMessageResponse> {
  try {
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
  } catch (error) {
    if (isAnonymousQuotaExceededError(error)) {
      const quota = readQuotaPayload(error.payload);

      return {
        status: "quota_exceeded",
        error: "anonymous_quota_exceeded",
        messages_remaining: quota.messages_remaining,
        messages_limit: quota.messages_limit,
      };
    }

    throw error;
  }
}
