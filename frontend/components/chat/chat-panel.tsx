"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { getCurrentUser } from "@/services/auth-service";
import { Bot, SendHorizontal, User } from "lucide-react";

import { sendMessage } from "@/services/chat-service";
import { useChat } from "@/context/ChatContext";

import {
  loadSessionId,
  saveSessionId,
} from "@/storage/chat-storage";

import ChatHistory from "./chat-history";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  time: string;
};

const WELCOME_MESSAGE: Message = {
  id: "welcome",
  role: "assistant",
  content: "Bonjour ! Je suis l'assistant TDE. Comment puis-je vous aider ?",
  time: "",
};

function now() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export default function ChatPanel() {
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [userId, setUserId] = useState<number | null>(null);

  // ---- State local d'affichage (source de vérité pour le rendu) ----
  const [messages, setMessages] = useState<Message[]>([WELCOME_MESSAGE]);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const {
    conversationId,
    setConversationId,
    selectedConversationId,
    setSelectedConversationId,
    conversations,
    setConversations,
    sessionId,
    setSessionId,
    createConversation,
  } = useChat();

  const isAuthenticated = userId !== null;

  // ---- Persistance : ajoute des messages à une conversation du context ----
  function appendMessagesToConversation(conversationId: number, newMessages: Message[]) {
    setConversations(prev =>
      prev.map(conversation =>
        conversation.conversationId !== conversationId
          ? conversation
          : { ...conversation, messages: [...conversation.messages, ...newMessages] }
      )
    );
  }

  // ---- Sélection d'une conversation dans l'historique ----
  function handleConversationSelect(conversationId: number) {
    setSelectedConversationId(conversationId);
    setConversationId(conversationId);
  }

  // ---- Synchronisation local <- context, uniquement au changement de conversation ----
  useEffect(() => {
    if (selectedConversationId === null) {
      setMessages([WELCOME_MESSAGE]);
      return;
    }
    const conversation = conversations.find(
      c => c.conversationId === selectedConversationId
    );
    if (conversation) {
      setMessages(conversation.messages);
    }
    // Volontairement dépendant de selectedConversationId seul :
    // on ne veut pas écraser l'optimistic update pendant un envoi en cours.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedConversationId]);

  // ---- Session utilisateur (auth) ----
  useEffect(() => {
    async function loadUser() {
      try {
        const response = await getCurrentUser();
        setUserId(Number(response.user.id));
      } catch {
        setUserId(null);
      }
    }
    loadUser();
  }, []);

  // ---- Session anonyme (sessionId) ----
  useEffect(() => {
    let savedSession = loadSessionId();
    if (!savedSession) {
      savedSession = `session_${crypto.randomUUID()}`;
      saveSessionId(savedSession);
    }
    setSessionId(savedSession);
  }, []);

  // ---- Auto-scroll ----
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isSending]);

  // ---- Envoi d'un message ----
  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!sessionId) return;

    const cleanedMessage = input.trim();
    if (!cleanedMessage || isSending) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: cleanedMessage,
      time: now(),
    };

    setInput("");
    setIsSending(true);

    // 1. Affichage immédiat
    setMessages(prev => [...prev, userMessage]);

    // 2. Persistance (context), sans bloquer l'affichage
    const isNewConversation = conversationId === null;
    let currentConversationId = conversationId;

    if (currentConversationId !== null) {
      appendMessagesToConversation(currentConversationId, [userMessage]);
    } else {
      createConversation({
        conversationId: -1,
        title: cleanedMessage,
        createdAt: new Date().toISOString(),
        messages: [WELCOME_MESSAGE, userMessage],
      });
      currentConversationId = -1;
    }

    try {
      const result = await sendMessage(
        cleanedMessage,
        sessionId,
        currentConversationId === -1 ? null : currentConversationId
      );
      const botData = result.data;

      if (botData.conversation_id && conversationId === null) {
        setConversationId(botData.conversation_id);
        setSelectedConversationId(botData.conversation_id);
        currentConversationId = botData.conversation_id;
      }

      const botMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: botData.response,
        time: now(),
      };

      // 1. Affichage immédiat
      setMessages(prev => [...prev, botMessage]);

      // 2. Persistance
      if (isNewConversation) {
        setConversations(prev =>
          prev.map(c =>
            c.conversationId === -1
              ? {
                  ...c,
                  conversationId: botData.conversation_id,
                  title: cleanedMessage,
                  messages: [...c.messages, botMessage],
                }
              : c
          )
        );
      } else {
        appendMessagesToConversation(currentConversationId!, [botMessage]);
      }

      if (botData.ticket_proposal) {
        const ticketMessage: Message = {
          id: crypto.randomUUID(),
          role: "assistant",
          content: "Souhaitez-vous un suivi auprès de la TDE ? Répondez Oui ou Non.",
          time: now(),
        };
        setMessages(prev => [...prev, ticketMessage]);
        appendMessagesToConversation(currentConversationId!, [ticketMessage]);
      }
    } catch (error) {
      console.error(error);
      const errorMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: "Une erreur est survenue. Veuillez réessayer.",
        time: now(),
      };
      setMessages(prev => [...prev, errorMessage]);
      if (conversationId) {
        appendMessagesToConversation(conversationId, [errorMessage]);
      }
    } finally {
      setIsSending(false);
    }
  }

  return (
    <main className="flex h-[calc(100vh-80px)] flex-col">
      {/* ZONE DE CHAT */}
      <div
        className="
          flex-1 overflow-y-auto px-3 py-8 sm:px-6 lg:px-10
          [scrollbar-width:none] [-ms-overflow-style:none]
          [&::-webkit-scrollbar]:hidden
        "
      >
        <div className="mx-auto flex w-full max-w-4xl flex-col gap-8">
          {messages.map((message) => {
            const isUser = message.role === "user";
            return (
              <div
                key={message.id}
                className={`flex w-full items-end gap-3 ${isUser ? "justify-end" : "justify-start"}`}
              >
                {!isUser && (
                  <div className="hidden h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#e8f7f1] text-[#1FA97A] sm:flex">
                    <Bot className="h-5 w-5" />
                  </div>
                )}

                <div className={`flex max-w-[78%] flex-col ${isUser ? "items-end" : "items-start"}`}>
                  <div
                    className={`
                      relative rounded-[22px] px-5 py-3.5 shadow-[0_2px_8px_rgba(0,0,0,0.04)]
                      ${isUser
                        ? "bg-[#1FA97A] text-white after:absolute after:-right-1 after:bottom-3 after:h-4 after:w-4 after:rotate-45 after:rounded-[3px] after:bg-[#1FA97A]"
                        : "border border-[#eceff3] bg-white text-[#111827] after:absolute after:-left-1 after:bottom-3 after:h-4 after:w-4 after:rotate-45 after:rounded-[3px] after:border-l after:border-b after:border-[#eceff3] after:bg-white"
                      }
                    `}
                  >
                    <p className="whitespace-pre-wrap break-words text-[15px] leading-relaxed">
                      {message.content}
                    </p>
                  </div>
                  <span className="mt-1.5 px-2 text-[11px] text-[#9ca3af]">{message.time}</span>
                </div>

                {isUser && (
                  <div className="hidden h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#e8f7f1] text-[#1FA97A] sm:flex">
                    <User className="h-5 w-5" />
                  </div>
                )}
              </div>
            );
          })}

          {isSending && (
            <div className="flex items-end gap-3">
              <div className="hidden h-10 w-10 items-center justify-center rounded-full bg-[#e8f7f1] text-[#1FA97A] sm:flex">
                <Bot className="h-5 w-5" />
              </div>
              <div
                className="
                  relative rounded-[22px] border border-[#eceff3] bg-white px-5 py-3.5
                  shadow-[0_2px_8px_rgba(0,0,0,0.04)]
                  after:absolute after:-left-1 after:bottom-3 after:h-4 after:w-4 after:rotate-45
                  after:rounded-[3px] after:border-l after:border-b after:border-[#eceff3] after:bg-white
                "
              >
                <div className="flex gap-1">
                  <span className="h-2 w-2 animate-bounce rounded-full bg-[#1FA97A]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-[#1FA97A] [animation-delay:0.2s]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-[#1FA97A] [animation-delay:0.4s]" />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* ZONE DE SAISIE */}
      <div className="sticky bottom-0 z-20 px-3 pb-5 pt-3 sm:px-6 lg:px-10">
        <div className="mx-auto w-full max-w-4xl">
          <form
            onSubmit={handleSubmit}
            className="
              flex items-end gap-3 rounded-[30px] border border-[#e5e7eb] bg-white/90 p-3
              shadow-[0_8px_30px_rgba(0,0,0,0.06)] backdrop-blur-xl transition-all duration-200
              focus-within:border-[#1FA97A] focus-within:shadow-[0_0_0_4px_rgba(31,169,122,0.12)]
            "
          >
            <div className="flex flex-1 items-center">
              <textarea
                value={input}
                onChange={(event) => setInput(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" && !event.shiftKey) {
                    event.preventDefault();
                    if (input.trim() && !isSending) {
                      handleSubmit(event as unknown as FormEvent<HTMLFormElement>);
                    }
                  }
                }}
                rows={1}
                placeholder="Posez votre question..."
                className="
                  max-h-40 min-h-[24px] flex-1 resize-none bg-transparent px-2 py-2
                  text-[15px] leading-relaxed text-[#111827] outline-none
                  placeholder:text-[#9ca3af]
                  [scrollbar-width:none] [-ms-overflow-style:none]
                  [&::-webkit-scrollbar]:hidden
                "
              />
            </div>

            <button
              type="submit"
              disabled={!input.trim() || isSending}
              className="
                flex h-12 w-12 shrink-0 items-center justify-center rounded-full
                bg-[#1FA97A] text-white shadow-[0_4px_14px_rgba(31,169,122,0.35)]
                transition-all duration-200 hover:scale-105 hover:bg-[#16956b]
                active:scale-95 disabled:cursor-not-allowed disabled:opacity-50
              "
            >
              <SendHorizontal className="h-5 w-5" />
            </button>
          </form>

          <div className="mt-3 text-center text-[11px] text-[#b0b7c3]">
            🔒 Conversations sécurisées
          </div>
        </div>
      </div>
    </main>
  );
}