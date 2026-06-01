"use client";

import { FormEvent, useEffect, useRef, useState } from "react";

import {
  Bot,
  SendHorizontal,
  User,
} from "lucide-react";

import { sendMessage } from "@/services/chat-service";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  time: string;
};
const STORAGE_KEY = "tde_chat_messages";
const SESSION_KEY = "tde_chat_session";

export default function ChatPanel() {

  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);

  const [messages, setMessages] = useState<Message[]>([]);
  useEffect(() => {

  const savedMessages =
    localStorage.getItem(STORAGE_KEY);

  if (savedMessages) {

    setMessages(
      JSON.parse(savedMessages)
    );

  } else {

    setMessages([
      {
        id: crypto.randomUUID(),
        role: "assistant",
        content:
          "Bonjour ! Je suis l'assistant TDE. Comment puis-je vous aider ?",
        time: "09:30",
      },
    ]);

  }

}, []);
useEffect(() => {

  if (messages.length > 0) {

    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(messages)
    );

  }

}, [messages]);
  const messagesEndRef =
    useRef<HTMLDivElement | null>(null);

  const [sessionId, setSessionId] = useState("");
  useEffect(() => {

  let savedSession =
    localStorage.getItem(SESSION_KEY);

  if (!savedSession) {

    savedSession =
      `session_${crypto.randomUUID()}`;

    localStorage.setItem(
      SESSION_KEY,
      savedSession
    );

  }

  setSessionId(savedSession);

}, []);
  const userId = "user_1";

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

    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);

    setInput("");
    setIsSending(true);

    try {

      const response = await sendMessage(
        cleanedMessage,
        sessionId,
        userId
      );

      const botMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response,
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setMessages((prev) => [
        ...prev,
        botMessage,
      ]);

    } catch (error) {

      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "Une erreur est survenue. Veuillez réessayer.",
          time: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);

    } finally {

      setIsSending(false);

    }
  }

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

                    <p
                      className="
                        whitespace-pre-wrap
                        break-words
                        text-[15px]
                        leading-relaxed
                      "
                    >
                      {message.content}
                    </p>

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