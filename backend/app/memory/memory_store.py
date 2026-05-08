from backend.app.memory.conversation_memory import ConversationMemory

# Store global en RAM : { session_id -> ConversationMemory }
_memory_store: dict[str, ConversationMemory] = {}


def get_memory(session_id: str) -> ConversationMemory:
    """Retourne la mémoire existante ou en crée une nouvelle."""
    if session_id not in _memory_store:
        _memory_store[session_id] = ConversationMemory(window_size=5)
    return _memory_store[session_id]


def clear_memory(session_id: str):
    """Supprime la mémoire d'une session terminée."""
    if session_id in _memory_store:
        _memory_store[session_id].reset()
        del _memory_store[session_id]