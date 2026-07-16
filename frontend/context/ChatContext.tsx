"use client";
import {
    createContext,
    useContext,
    useState,
    ReactNode,
} from "react";
import { saveSessionId } from "@/storage/chat-storage";
type ChatContextType = {
    conversationId: number | null;
    setConversationId: (id: number | null) => void;

    selectedConversationId: number | null;
    setSelectedConversationId: (
        id: number | null
    ) => void;

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
    const [sessionId, setSessionId] =
    useState<string | null>(null);
    function newConversation() {
        const newSession =
            `session_${crypto.randomUUID()}`;
        saveSessionId(newSession);
        setSessionId(newSession);
        setConversationId(null);
        setSelectedConversationId(null);
}

    return (
        <ChatContext.Provider
            value={{
            conversationId,
            setConversationId,

            selectedConversationId,
            setSelectedConversationId,

            newConversation,

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