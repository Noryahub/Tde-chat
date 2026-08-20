"use client";

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

   const messagesEndRef =
      useRef<HTMLDivElement>(null);



    const { isAuthenticated } = useAuth();

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
      if (botData.ticket_proposal) {

        const ticketMessage: Message = {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "Souhaitez-vous un suivi auprès de la TDE ? Répondez Oui ou Non.",
          time: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        };
    appendMessagesToConversation(
            currentConversationId!,
            [ticketMessage]
        );
      }

    } catch (error) {

      console.error(error);
        const errorMessage: Message = {
            id: crypto.randomUUID(),
            role: "assistant",
            content:
                "Une erreur est survenue. Veuillez réessayer.",
            time: new Date().toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
            }),
        };

        if (conversationId) {
            appendMessagesToConversation(
                conversationId,
                [errorMessage]
            );
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