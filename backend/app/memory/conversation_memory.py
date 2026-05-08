from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Turn:
    role: str                          # "user" ou "bot"
    content: str
    intent: Optional[str] = None
    confidence: Optional[float] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class ConversationMemory:
    """
    Mémoire conversationnelle à fenêtre glissante (RAM).
    Fenêtre de 5 tours = 10 messages max en contexte actif.
    """

    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.history: deque[Turn] = deque(maxlen=window_size * 2)
        self.session_context: dict = {}   # entités persistantes de la session
        self.current_intent: Optional[str] = None

    def add_user_turn(self, content: str, intent: str = None, confidence: float = None):
        self.history.append(Turn(
            role="user",
            content=content,
            intent=intent,
            confidence=confidence
        ))
        if intent:
            self.current_intent = intent

    def add_bot_turn(self, content: str):
        self.history.append(Turn(role="bot", content=content))

    def update_context(self, entities: dict):
        """Mémorise les entités importantes pour toute la session."""
        for key, value in entities.items():
            if value:
                self.session_context[key] = value

    def get_history_as_text(self) -> str:
        """Historique formaté pour injection dans le prompt LLM plus tard."""
        lines = []
        for turn in self.history:
            prefix = "Client" if turn.role == "user" else "Assistant"
            lines.append(f"{prefix}: {turn.content}")
        return "\n".join(lines)

    def get_last_intent(self) -> Optional[str]:
        return self.current_intent

    def get_context(self) -> dict:
        return self.session_context

    def reset(self):
        self.history.clear()
        self.session_context.clear()
        self.current_intent = None

    def load_from_db(self, db_history: list):
        """
        Reconstruit la mémoire depuis l'historique DB.
        db_history : liste de dicts avec clés 'user_message', 'bot_response',
                     'intent', 'confidence'
        Appelé au démarrage d'une session existante.
        """
        for row in db_history[-self.window_size:]:  # on garde les N derniers
            self.add_user_turn(
                content=row["user_message"],
                intent=row.get("intent"),
                confidence=row.get("confidence")
            )
            self.add_bot_turn(content=row["bot_response"])