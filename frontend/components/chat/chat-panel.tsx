"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { SendHorizontal } from "lucide-react";

import { sendMessage } from "@/services/chat-service";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  time: string;
};

export default function ChatPanel() {

  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);

  const [messages, setMessages] = useState<Message[]>([
    {
      id: crypto.randomUUID(),
      role: "assistant",
      content:
        "Bonjour 👋 Je suis l'assistant TDE. Comment puis-je vous aider ?",
      time: "",
    },
  ]);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const sessionId = "session_1";
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

    const cleanedMessage = input.trim();

    if (!cleanedMessage || isSending) {
      return;
    }

    const now = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    // =========================================
    // USER MESSAGE
    // =========================================

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
        h-screen
        items-center
        justify-center
        bg-[#e5e5e5]
        p-6
      "
    >

      <section
        className="
          flex
          h-[92vh]
          w-full
          max-w-5xl
          flex-col
          overflow-hidden
          rounded-[28px]
          border
          border-black/10
          bg-[#f3f3f3]
          shadow-2xl
        "
      >

        {/* ========================================= */}
        {/* HEADER */}
        {/* ========================================= */}

        <div
          className="
            flex
            items-center
            gap-4
            bg-[#1D9E75]
            px-6
            py-5
          "
        >

          <div
            className="
              flex
              h-12
              w-12
              items-center
              justify-center
              rounded-full
              bg-white/20
              text-lg
            "
          >
            😊
          </div>

          <div>

            <h1 className="text-lg font-semibold text-white">
              Assistant
            </h1>

            <div
              className="
                mt-1
                flex
                items-center
                gap-2
                text-sm
                text-white/80
              "
            >

              <span
                className="
                  h-2
                  w-2
                  rounded-full
                  bg-[#b8f5d6]
                "
              />

              En ligne

            </div>

          </div>

        </div>

        {/* ========================================= */}
        {/* CHAT AREA */}
        {/* ========================================= */}

        <div
          className="
            flex-1
            overflow-y-auto
            px-8
            py-6
          "
        >

          <div className="flex flex-col gap-6">

            {messages.map((message) => {

              const isUser =
                message.role === "user";

              return (

                <div
                  key={message.id}
                  className={`flex ${
                    isUser
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >

                  <div
                    className={`
                      max-w-[70%]
                      rounded-[20px]
                      px-5
                      py-4
                      text-sm
                      shadow-sm
                      ${
                        isUser
                          ? "bg-[#1D9E75] text-white"
                          : "border border-black/10 bg-white text-black"
                      }
                    `}
                  >

                    <p className="leading-relaxed whitespace-pre-wrap break-words">
                      {message.content}
                    </p>

                    <div
                      className={`
                        mt-2
                        text-right
                        text-[11px]
                        ${
                          isUser
                            ? "text-white/70"
                            : "text-neutral-400"
                        }
                      `}
                    >
                      {message.time}
                    </div>

                  </div>

                </div>
              );
            })}

            {/* ========================================= */}
            {/* TYPING */}
            {/* ========================================= */}

            {isSending && (

              <div className="flex justify-start">

                <div
                  className="
                    rounded-[20px]
                    bg-white
                    px-4
                    py-3
                    shadow-sm
                  "
                >

                  <div className="flex gap-1">

                    <span
                      className="
                        h-2
                        w-2
                        animate-bounce
                        rounded-full
                        bg-[#1D9E75]
                      "
                    />

                    <span
                      className="
                        h-2
                        w-2
                        animate-bounce
                        rounded-full
                        bg-[#1D9E75]
                        [animation-delay:0.2s]
                      "
                    />

                    <span
                      className="
                        h-2
                        w-2
                        animate-bounce
                        rounded-full
                        bg-[#1D9E75]
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
        {/* FOOTER */}
        {/* ========================================= */}

        <div
          className="
            border-t
            border-black/10
            bg-[#f7f7f7]
            px-6
            py-5
          "
        >

          <form
            onSubmit={handleSubmit}
            className="
              flex
              items-center
              gap-4
            "
          >

            <input
              value={input}
              onChange={(event) =>
                setInput(event.target.value)
              }
              placeholder="Écrivez votre message..."
              className="
                h-14
                flex-1
                rounded-full
                border
                border-black/10
                bg-white
                px-6
                text-sm
                outline-none
                transition-all
                focus:border-[#1D9E75]
                focus:ring-4
                focus:ring-[#1D9E75]/10
              "
            />

            <button
              type="submit"
              disabled={
                !input.trim() || isSending
              }
              className="
                flex
                h-14
                items-center
                justify-center
                gap-2
                rounded-full
                bg-[#1D9E75]
                px-8
                text-sm
                font-medium
                text-white
                transition-all
                hover:bg-[#157a5b]
                disabled:cursor-not-allowed
                disabled:opacity-50
              "
            >

              <SendHorizontal className="h-4 w-4" />

              Envoyer

            </button>

          </form>

          <div
            className="
              mt-4
              text-center
              text-[11px]
              text-neutral-400
            "
          >
            🔒 Chiffré de bout en bout
          </div>

        </div>

      </section>

    </main>
  );
}