import { getConversationHistory } from "@/services/history-service";

import type {
  History,
  Message,
} from "@/types";

const STORAGE_KEY = "tde_chat_messages";
const SESSION_KEY = "tde_chat_session";

/* ==================
   Conversion History
   ========================*/

function historyToMessages(
  history: History[]
): ChatMessage[] {

  return history.map((item) => ({

    id: item.message_id.toString(),
    conversationId: item.conversation_id,
    role: item.role,
    content: item.content,
    createdAt: item.created_at,

  }));

}

/* =======================================================
   Chargement des messages
======================================================= */

export async function loadMessages(
  isAuthenticated: boolean,
  userId?: number
): Promise<Message[]> {

  // ==========================
  // Utilisateur connecté
  // ==========================

  if (isAuthenticated && userId) {

    try {

      const response =
        await getConversationHistory(userId);
        console.log("HISTORY =", response.data);
        // Regroupement par conversation
        const conversations =
          groupHistoryByConversation(
            response.data
          );

        console.log(
          "CONVERSATIONS =",
          conversations
        );
        return historyToMessages(
            response.data
        );
    } catch (error) {

      console.error(
        "Erreur lors du chargement de l'historique :",
        error
      );
      return [];
    }

  }

  // ==========================
  // Utilisateur anonyme
  // ==========================

  try {

    const data =
      sessionStorage.getItem(STORAGE_KEY);

    if (!data) {
      return [];
    }
    return JSON.parse(data);

  } catch {
    return [];

  }

}

/* =======================================================
   Sauvegarde des messages
======================================================= */

export async function saveMessages(
  messages: Message[],
  isAuthenticated: boolean
): Promise<void> {

  // Les utilisateurs connectés sont
  // automatiquement sauvegardés
  // par l'API /chat.
  if (isAuthenticated) {

    return;

  }

  // Utilisateur anonyme

  sessionStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(messages)
  );

}

/* =======================================================
   Suppression des messages
======================================================= */

export async function clearMessages(
  isAuthenticated: boolean
): Promise<void> {

  // Les conversations des utilisateurs
  // connectés restent dans la base.
  // On ne les supprime pas.

  if (isAuthenticated) {

    return;

  }

  sessionStorage.removeItem(
    STORAGE_KEY
  );

}

/* =======================================================
   Session
======================================================= */

export function loadSessionId():
string | null {

  return sessionStorage.getItem(
    SESSION_KEY
  );

}

export function saveSessionId(
  sessionId: string
): void {

  sessionStorage.setItem(
    SESSION_KEY,
    sessionId
  );

}

export function clearSessionId():
void {

  sessionStorage.removeItem(
    SESSION_KEY
  );

}

/* =======================================================
   Nettoyage complet
======================================================= */

export async function clearChatStorage(
  isAuthenticated: boolean
): Promise<void> {

  await clearMessages(
    isAuthenticated
  );

  clearSessionId();

}

function groupHistoryByConversation(
  history: History[]
): Conversation[] {

  const conversations =
    new Map<number, Conversation>();

  history.forEach((item) => {

    if (!conversations.has(item.conversation_id)) {

      conversations.set(
        item.conversation_id,
        {
          conversationId: item.conversation_id,

          title: "",

          createdAt: item.created_at,

          messages: [],
        }
      );

    }

    const conversation =
      conversations.get(item.conversation_id)!;

    const message: ChatMessage = {

      id: item.message_id.toString(),
      conversationId: item.conversation_id,
      role: item.role,
      content: item.content,
      createdAt: item.created_at,

    };

    conversation.messages.push(message);

    /**
     * Le premier message utilisateur
     * devient le titre de la conversation.
     */

    if (
      conversation.title === "" &&
      item.role === "user"
    ) {

      conversation.title = item.content;

    }

  });

  return Array.from(
    conversations.values()
  );

}
/* =======================================================
   Chargement des conversations
======================================================= */

export async function loadConversations(
  userId: number
): Promise<Conversation[]> {

  try {

    const response =
      await getConversationHistory(userId);

    return groupHistoryByConversation(
      response.data
    );

  } catch (error) {

    console.error(
      "Erreur chargement conversations :",
      error
    );

    return [];

  }

}