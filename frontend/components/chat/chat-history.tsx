"use client";

import type { Conversation } from "@/types";

type ChatHistoryProps = {
  conversations: Conversation[];
  selectedConversationId: number | null;
  onSelect: (conversationId: number) => void;
};

export default function ChatHistory({
  conversations,
  selectedConversationId,
  onSelect,
}: ChatHistoryProps) {

  return (

    <div className="space-y-2">

      <h2
        className="
          mb-4
          text-sm
          font-semibold
          text-gray-500
        "
      >
        Historique
      </h2>

      {conversations.map((conversation) => (

        <button
          key={conversation.conversationId}

          onClick={() =>
            onSelect(
              conversation.conversationId
            )
          }

          className={`
            w-full
            rounded-lg
            px-3
            py-3
            text-left
            transition

            ${
              selectedConversationId ===
              conversation.conversationId

                ? "bg-[#1FA97A] text-white"

                : "hover:bg-gray-100"
            }
          `}
        >

          <div
            className="
              truncate
              text-sm
              font-medium
            "
          >
            {conversation.title}
          </div>

          <div
            className="
              mt-1
              text-xs
              opacity-70
            "
          >
            {new Date(
              conversation.createdAt
            ).toLocaleDateString()}
          </div>

        </button>

      ))}

    </div>

  );

}