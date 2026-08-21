"use client";

import Link from "next/link";
import { FormEvent, useEffect, useRef, useState } from "react";
import { useAuth } from "@/hooks/use-auth";
import {
  Bot,
  SendHorizontal,
  User,
} from "lucide-react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { sendMessage } from "@/services/chat-service";
import { ApiError } from "@/services/api";
import type {Conversation} from "@/types"
import { useChat } from "@/context/ChatContext";

import {
  loadMessages,
  saveMessages,
  loadSessionId,
  saveSessionId,
  clearChatStorage,
  loadConversations
} from "@/storage/chat-storage";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  time: string;
};
const WELCOME_MESSAGE: Message = {
    id: "welcome",
    role: "assistant",
    content:
        "Bonjour ! Je suis l'assistant TDE. Comment puis-je vous aider ?",
    time: "",
};

import ChatHistory
from "./chat-history";

export default function ChatPanel() {

  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [quotaExceeded, setQuotaExceeded] = useState(false);

   const messagesEndRef =
      useRef<HTMLDivElement>(null);



    const {
        isAuthenticated,
        loginWithGoogle,
    } = useAuth();

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

    const currentConversation =
        conversations.find(
        (   conversation) =>
                conversation.conversationId ===
                selectedConversationId
    );

    const welcomeMessage: Message = {
        id: "welcome",
        role: "assistant",
        content:
            "Bonjour ! Je suis l'assistant TDE. Comment puis-je vous aider ?",
        time: "",
    };

    const messages =
        currentConversation?.messages ??
        [WELCOME_MESSAGE];
        console.log("selectedConversationId =", selectedConversationId);
        console.log("currentConversation =", currentConversation);
        console.log("messages =", messages);

        function handleConversationSelect(
            conversationId: number
        ) {
            setSelectedConversationId(
                conversationId
            );
            setConversationId(
                conversationId
            );
        }



useEffect(() => {
    console.log(
        "CONVERSATIONS",
        conversations
    );
}, [conversations]);
useEffect(() => {
    if (messages.length === 0) {
        return;
    }
    saveMessages(
        messages,
        isAuthenticated
    );
}, [
    messages,
    isAuthenticated,
]);

useEffect(() => {
    let savedSession = loadSessionId();
    if (!savedSession) {
        savedSession =
            `session_${crypto.randomUUID()}`;
        saveSessionId(savedSession);
    }
    setSessionId(savedSession);
}, []);

async function handleGoogleLogin() {
    let currentSessionId = sessionId || loadSessionId();

    if (!currentSessionId) {
        currentSessionId =
            `session_${crypto.randomUUID()}`;
        saveSessionId(currentSessionId);
        setSessionId(currentSessionId);
    }

    await loginWithGoogle(
        currentSessionId,
        "/user/chat"
    );
}
  // =========================================
  // AUTO SCROLL
  // =========================================

  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages, isSending]);

  // =========================================


  // SEND MESSAGE
  // =========================================
        function appendMessagesToConversation(
                conversationId: number,
                newMessages: Message[]
            ) {
                setConversations(prev =>
                    prev.map(conversation => {

                        if (
                            conversation.conversationId !== conversationId
                        ) {
                            return conversation;
                        }

                        return {
                            ...conversation,
                            messages: [
                                ...conversation.messages,
                                ...newMessages,
                            ],
                        };

                    })
                );
            }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();
    if (!sessionId) {
        return;
    }
    const cleanedMessage = input.trim();

    if (!cleanedMessage || isSending) {
      return;
    }

    const now = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: cleanedMessage,
      time: now,
    };
    setInput("");
    setIsSending(true);
    let currentConversationId = conversationId;
        // Affichage immédiat du message utilisateur
           if (currentConversationId !== null) {
                appendMessagesToConversation(
                    currentConversationId,
                    [userMessage]
                );
            } else {
                createConversation({
                    conversationId: -1,
                    title: cleanedMessage,
                    createdAt: new Date().toISOString(),
                    messages: [
                        welcomeMessage,
                        userMessage,
                    ],
                });

                currentConversationId = -1;

            }
        const isNewConversation = conversationId === null;
     try {
      setQuotaExceeded(false);

      const result = await sendMessage(
            cleanedMessage,
            sessionId!,
            currentConversationId === -1
                ? null
                : currentConversationId
        );

      const botData = result.data;
      if (
        botData.conversation_id &&
        conversationId === null
    ) {
        setConversationId(
            botData.conversation_id
        );
        currentConversationId =
             botData.conversation_id;
    }
      const botMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: botData.response,
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };
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
            currentConversationId = botData.conversation_id;
            setConversationId(botData.conversation_id);
            setSelectedConversationId(botData.conversation_id);

        } else {

            appendMessagesToConversation(
                currentConversationId!,
                [botMessage]
            );

        }

      console.log("BOT DATA :", botData);

    } catch (error) {

      console.error(error);
        const quotaExceeded =
            error instanceof ApiError &&
            error.status === 429 &&
            error.code === "anonymous_quota_exceeded";

        setQuotaExceeded(quotaExceeded);

        if (!quotaExceeded) {
            const errorMessage: Message = {
                id: crypto.randomUUID(),
                role: "assistant",
                content: "Une erreur est survenue. Veuillez réessayer.",
                time: new Date().toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                }),
            };

            if (currentConversationId !== null) {
                appendMessagesToConversation(
                    currentConversationId,
                    [errorMessage]
                );
            }
        }

    } finally {
      setIsSending(false);
    }
  }
  console.log("messages", messages);

  return (

    <main
      className="
        flex
        h-[calc(100vh-80px)]
        flex-col
      "
    >

      {/* ========================================= */}
      {/* CHAT AREA */}
      {/* ========================================= */}

      <div
        className="
          flex-1
          overflow-y-auto
          px-3
          py-8
          sm:px-6
          lg:px-10
          [scrollbar-width:none]
          [-ms-overflow-style:none]
          [&::-webkit-scrollbar]:hidden
        "
      >

        <div
          className="
            mx-auto
            flex
            w-full
            max-w-4xl
            flex-col
            gap-8
          "
        >

          {messages.map((message) => {

            const isUser =
              message.role === "user";

            return (

              <div
                key={message.id}
                className={`
                  flex
                  w-full
                  items-end
                  gap-3
                  ${
                    isUser
                      ? "justify-end"
                      : "justify-start"
                  }
                `}
              >

                {/* ========================================= */}
                {/* ASSISTANT AVATAR */}
                {/* ========================================= */}

                {!isUser && (

                  <div
                    className="
                      hidden
                      h-10
                      w-10
                      shrink-0
                      items-center
                      justify-center
                      rounded-full
                      bg-[#e8f7f1]
                      text-[#1FA97A]
                      sm:flex
                    "
                  >

                    <Bot className="h-5 w-5" />

                  </div>
                )}

                {/* ========================================= */}
                {/* MESSAGE */}
                {/* ========================================= */}

                <div
                  className={`
                    flex
                    max-w-[78%]
                    flex-col
                    ${
                      isUser
                        ? "items-end"
                        : "items-start"
                    }
                  `}
                >

                  <div
                    className={`
                      relative
                      rounded-[22px]
                      px-5
                      py-3.5
                      shadow-[0_2px_8px_rgba(0,0,0,0.04)]

                      ${
                        isUser
                          ? `
                            bg-[#1FA97A]
                            text-white

                            after:absolute
                            after:-right-1
                            after:bottom-3
                            after:h-4
                            after:w-4
                            after:rotate-45
                            after:rounded-[3px]
                            after:bg-[#1FA97A]
                          `
                          : `
                            border
                            border-[#eceff3]
                            bg-white
                            text-[#111827]

                            after:absolute
                            after:-left-1
                            after:bottom-3
                            after:h-4
                            after:w-4
                            after:rotate-45
                            after:rounded-[3px]
                            after:border-l
                            after:border-b
                            after:border-[#eceff3]
                            after:bg-white
                          `
                      }
                    `}
                  >

                    <div className="text-[15px] leading-relaxed">
<ReactMarkdown
  remarkPlugins={[remarkGfm]}
  components={{
    p: ({ children }) => (
      <p className="mb-3 last:mb-0">
        {children}
      </p>
    ),

    strong: ({ children }) => (
      <strong className="font-semibold">
        {children}
      </strong>
    ),

    ol: ({ children }) => (
      <ol className="mb-3 ml-5 list-decimal space-y-2">
        {children}
      </ol>
    ),

    ul: ({ children }) => (
      <ul className="mb-3 ml-5 list-disc space-y-2">
        {children}
      </ul>
    ),

    li: ({ children }) => (
      <li className="pl-1">
        {children}
      </li>
    ),

    table: ({ children }) => (
      <div className="my-4 w-full overflow-x-auto">
        <table className="w-full min-w-[600px] border-collapse text-sm">
          {children}
        </table>
      </div>
    ),

    thead: ({ children }) => (
      <thead className="bg-[#f5f7f9]">
        {children}
      </thead>
    ),

    tbody: ({ children }) => (
      <tbody>
        {children}
      </tbody>
    ),

    tr: ({ children }) => (
      <tr className="border-b border-[#eceff3]">
        {children}
      </tr>
    ),

    th: ({ children }) => (
      <th className="border border-[#e5e7eb] px-3 py-2 text-left font-semibold text-[#374151]">
        {children}
      </th>
    ),

    td: ({ children }) => (
      <td className="border border-[#e5e7eb] px-3 py-2 align-top text-[#4b5563]">
        {children}
      </td>
    ),
  }}
>
  {message.content}
</ReactMarkdown>
</div>

                  </div>

                  <span
                    className="
                      mt-1.5
                      px-2
                      text-[11px]
                      text-[#9ca3af]
                    "
                  >
                    {message.time}
                  </span>

                </div>

                {/* ========================================= */}
                {/* USER AVATAR */}
                {/* ========================================= */}

                {isUser && (

                  <div
                    className="
                      hidden
                      h-10
                      w-10
                      shrink-0
                      items-center
                      justify-center
                      rounded-full
                      bg-[#e8f7f1]
                      text-[#1FA97A]
                      sm:flex
                    "
                  >

                    <User className="h-5 w-5" />

                  </div>
                )}

              </div>
            );
          })}

          {/* ========================================= */}
          {/* TYPING */}
          {/* ========================================= */}

          {isSending && (

            <div
              className="
                flex
                items-end
                gap-3
              "
            >

              <div
                className="
                  hidden
                  h-10
                  w-10
                  items-center
                  justify-center
                  rounded-full
                  bg-[#e8f7f1]
                  text-[#1FA97A]
                  sm:flex
                "
              >

                <Bot className="h-5 w-5" />

              </div>

              <div
                className="
                  relative
                  rounded-[22px]
                  border
                  border-[#eceff3]
                  bg-white
                  px-5
                  py-3.5
                  shadow-[0_2px_8px_rgba(0,0,0,0.04)]

                  after:absolute
                  after:-left-1
                  after:bottom-3
                  after:h-4
                  after:w-4
                  after:rotate-45
                  after:rounded-[3px]
                  after:border-l
                  after:border-b
                  after:border-[#eceff3]
                  after:bg-white
                "
              >

                <div className="flex gap-1">

                  <span
                    className="
                      h-2
                      w-2
                      animate-bounce
                      rounded-full
                      bg-[#1FA97A]
                    "
                  />

                  <span
                    className="
                      h-2
                      w-2
                      animate-bounce
                      rounded-full
                      bg-[#1FA97A]
                      [animation-delay:0.2s]
                    "
                  />

                  <span
                    className="
                      h-2
                      w-2
                      animate-bounce
                      rounded-full
                      bg-[#1FA97A]
                      [animation-delay:0.4s]
                    "
                  />

                </div>

              </div>

            </div>
          )}

          <div ref={messagesEndRef} />

        </div>

      </div>

      {/* ========================================= */}
      {/* INPUT AREA */}
      {/* ========================================= */}

      {/* ========================================= */}
{/* INPUT AREA */}
{/* ========================================= */}

<div
  className="
    sticky
    bottom-0
    z-20
    px-3
    pb-5
    pt-3
    sm:px-6
    lg:px-10
  "
>

  <div
    className="
      mx-auto
      w-full
      max-w-4xl
    "
  >

    <form
      onSubmit={handleSubmit}
      className="
          flex
          items-end
          gap-3
          rounded-[30px]
          border
          border-[#e5e7eb]
          bg-white/90
          p-3
          shadow-[0_8px_30px_rgba(0,0,0,0.06)]
          backdrop-blur-xl
          transition-all
          duration-200

          focus-within:border-[#1FA97A]
          focus-within:shadow-[0_0_0_4px_rgba(31,169,122,0.12)]
        "
    >

      {/* INPUT */}

      <div className="flex flex-1 items-center">

        <textarea
                  value={input}
                  onChange={(event) =>
                    setInput(event.target.value)
                  }

                  onKeyDown={(event) => {

                    if (
                      event.key === "Enter" &&
                      !event.shiftKey
                    ) {

                      event.preventDefault();

                      if (
                        input.trim() &&
                        !isSending
                      ) {

                        handleSubmit(
                          event as unknown as FormEvent<HTMLFormElement>
                        );

                      }

                    }

                  }}

                  rows={1}
                  placeholder="Posez votre question..."
                  className="
                    max-h-40
                    min-h-[24px]
                    flex-1
                    resize-none
                    bg-transparent
                    px-2
                    py-2
                    text-[15px]
                    leading-relaxed
                    text-[#111827]
                    outline-none
                    placeholder:text-[#9ca3af]
                    [scrollbar-width:none]
                    [-ms-overflow-style:none]
                    [&::-webkit-scrollbar]:hidden
                  "
         />

      </div>

      {/* BUTTON */}

      <button
        type="submit"
        disabled={
          !input.trim() || isSending
        }
        className="
          flex
          h-12
          w-12
          shrink-0
          items-center
          justify-center
          rounded-full
          bg-[#1FA97A]
          text-white
          shadow-[0_4px_14px_rgba(31,169,122,0.35)]
          transition-all
          duration-200
          hover:scale-105
          hover:bg-[#16956b]
          active:scale-95
          disabled:cursor-not-allowed
          disabled:opacity-50
        "
      >

        <SendHorizontal className="h-5 w-5" />

      </button>

    </form>

    {quotaExceeded && !isAuthenticated && (
      <div
        className="
          mt-3
          rounded-2xl
          border
          border-[#f0d4a7]
          bg-[#fff8ec]
          px-4
          py-3
          text-sm
          text-[#6b3f00]
        "
      >
        <div className="font-semibold text-[#8a5a00]">
          Limite de messages atteinte
        </div>
        <p className="mt-1 leading-relaxed">
          Vous avez utilisé vos{" "}
          <strong className="font-semibold">5 messages gratuits</strong>.
          Connectez-vous pour continuer à utiliser l'assistant TDE.
        </p>

        <div className="mt-3 flex flex-wrap items-center gap-3">
          <Link
            href="/login"
            className="
              inline-flex
              h-10
              items-center
              justify-center
              rounded-lg
              bg-[#1FA97A]
              px-4
              font-medium
              text-white
              transition
              hover:bg-[#16956b]
            "
          >
            Se connecter
          </Link>

          <Link
            href="/register"
            className="
              inline-flex
              h-10
              items-center
              justify-center
              rounded-lg
              border
              border-[#d7b779]
              bg-white
              px-4
              font-medium
              text-[#1f2937]
              transition
              hover:bg-[#fff3db]
            "
          >
            Créer un compte
          </Link>

          <button
            type="button"
            onClick={handleGoogleLogin}
            className="
              inline-flex
              h-10
              items-center
              gap-2
              rounded-lg
              border
              border-[#d7b779]
              bg-white
              px-4
              font-medium
              text-[#1f2937]
              transition
              hover:bg-[#fff3db]
            "
          >
            <svg className="h-4 w-4" viewBox="0 0 24 24">
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
              />
            </svg>
            Continuer avec Google
          </button>
        </div>
      </div>
    )}

    {/* FOOTER */}

    <div
      className="
        mt-3
        text-center
        text-[11px]
        text-[#b0b7c3]
      "
    >
      🔒 Conversations sécurisées
    </div>
  </div>
</div>
</main>
  );
}
