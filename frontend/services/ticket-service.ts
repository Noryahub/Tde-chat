import { get, patch } from "@/services/api";
import type {
  ApiResponse,
  Ticket,
} from "@/types";

type TicketsResponse =
  ApiResponse<Ticket[]>;

export async function getTickets() {
  return get<TicketsResponse>(
    "/api/admin/tickets"
  );
}

export async function updateTicketStatus(
  ticketId: number,
  statut: string
) {
  return patch(
    `/tickets/${ticketId}/status`,
    {
      statut,
    }
  );
}


// Tous les signalements de l'utilisateur

export async function getUserSignalements(
  userId: number
): Promise<{
  status: string;
  data: Ticket[];
}> {

  return get(
    `/api/tickets/user/${userId}`
  );

}

// Signalements résolus


export async function getResolvedSignalements(
  userId: number
): Promise<{
  status: string;
  data: Ticket[];
}> {

  return get(
    `/api/tickets/user/${userId}/resolved`
  );

}