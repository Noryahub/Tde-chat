"use client";
import {
    createContext,
    useContext,
    useState,
    useEffect,
    ReactNode,
} from "react";

import { loadConversations } from "@/storage/chat-storage";
import { saveSessionId } from "@/storage/chat-storage";
import { useAuth } from "@/hooks/use-auth";
import type { Conversation } from "@/types";

type ChatContextType = {
    conversationId: number | null;
    setConversationId: (id: number | null) => void;

    selectedConversationId: number | null;
    setSelectedConversationId: (
        id: number | null
    ) => void;

    conversations: Conversation[];
    setConversations: React.Dispatch<
    React.SetStateAction<Conversation[]>
    >;

    sessionId: string | null;
    setSessionId: (
        id: string | null
    ) => void;

    newConversation: () => void;
    createConversation: (
        conversation: Conversation
    ) => void;
};

const ChatContext =
    createContext<
        ChatContextType | undefined
    >(undefined);

export function ChatProvider({
    children,
}:{
    children: ReactNode;
}){
    const [
        conversationId,
        setConversationId,
    ] = useState<number | null>(null);
    const [
        selectedConversationId,
        setSelectedConversationId,
    ] = useState<number | null>(null);

    const [
        conversations,
        setConversations,
    ] = useState<Conversation[]>([]);

    const [sessionId, setSessionId] =
    useState<string | null>(null);

    // ======================================
    // AUTHENTIFICATION — source unique : AuthProvider
    // ======================================
    const {
        user,
        isAuthenticated,
        isLoading: isAuthLoading,
    } = useAuth();

    const userId = user?.id ? Number(user.id) : null;

    // ======================================
    // FONCTIONS DE CONVERSATION
    // ======================================

    function newConversation() {
        console.log("NEW CONVERSATION");
        const newSession =
            `session_${crypto.randomUUID()}`;
        saveSessionId(newSession);
        setSessionId(newSession);
        setConversationId(null);
        setSelectedConversationId(null);
    }

    function createConversation(
        conversation: Conversation
    ) {
        console.log("CREATE", conversation.conversationId);
        setConversations(prev => [
            ...prev,
            conversation,
        ]);
    }

    // ======================================
    // CHARGEMENT DE L'HISTORIQUE
    // Attend que AuthProvider ait restauré la session
    // avant de charger les conversations.
    // ======================================
    useEffect(() => {
        // Attendre la fin de la restauration de la session
        if (isAuthLoading) {
            return;
        }

        // Utilisateur non connecté : vider l'historique
        if (!isAuthenticated || !userId) {
            setConversations([]);
            return;
        }

        // Utilisateur connecté : charger les conversations
        console.log("ChatProvider → loadConversations pour userId =", userId);
        async function loadHistory() {
            const history = await loadConversations(userId!);
            console.log("ChatProvider → setConversations", history.length, "conversations");
            setConversations(history);
        }

        loadHistory();
    }, [isAuthLoading, isAuthenticated, userId]);

    useEffect(() => {
        console.log(
            "ChatProvider conversations",
            conversations
        );
    }, [conversations]);

    return (
        <ChatContext.Provider
            value={{
            conversationId,
            setConversationId,

            selectedConversationId,
            setSelectedConversationId,

            newConversation,
            conversations,
            setConversations,
            sessionId,
            setSessionId,
            createConversation,
        }}
        >
            {children}
        </ChatContext.Provider>
    );
}

export function useChat(){
    const context =
        useContext(ChatContext);
    if(!context){
        throw new Error(
            "useChat doit être utilisé dans ChatProvider"
        );
    }
    return context;
}