from backend.app.services.chatbot_service import process_message


def send_message(user_message: str, session_id: str, user_id: int) -> str:
    """
    Appel direct au service backend (pas d'HTTP — même processus).
    Retourne la réponse du bot.
    """
    try:
        return process_message(
            user_message=user_message,
            session_id=session_id,
            user_id=str(user_id)
        )
    except Exception as e:
        print(f"Erreur chat_client : {e}")
        return "Une erreur est survenue. Veuillez réessayer."