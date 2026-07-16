"use client";
import {
    createContext,
    useContext,
    useState,
    ReactNode,
} from "react";

import { useEffect } from "react";
import { loadConversations } from "@/storage/chat-storage";
import { getCurrentUser } from "@/services/auth-service";

import { saveSessionId } from "@/storage/chat-storage";
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
    const [userId, setUserId] =
    useState<number | null>(null);

    function newConversation() {
        const newSession =
            `session_${crypto.randomUUID()}`;
        saveSessionId(newSession);
        setSessionId(newSession);
        setConversationId(null);
        setSelectedConversationId(null);
    }
        useEffect(() => {
            async function loadUser() {
                try {
                    const response =
                        await getCurrentUser();
                        console.log("CURRENT USER =", response);
                    setUserId(
                        Number(response.user.id)
                    );
                    console.log("USER ID =", Number(response.user.id));
                } catch {
                    setUserId(null);
                }
            }
            loadUser();
        }, []);

        useEffect(() => {
            async function initializeConversations() {
                    console.log("userId =", userId);
                    if (!userId) {
                        setConversations([]);
                        return;
                    }
                    const history =
                        await loadConversations(userId);
                    setConversations(history);
                }
                initializeConversations();
    }, [userId]);

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