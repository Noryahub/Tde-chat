import {get} from "@/services/api";
import type {
  ApiResponse,
  History
} from "@/types";

type HistoryResponse =  ApiResponse<History[]>;

export async function getConversationHistory(
  userId: number
): Promise<{
  status: string;
  data: History[];
}> {

  return get(
    `/history/user/${userId}`
  );

}