CONFIDENCE_THRESHOLD = 0.4

NEUTRAL_FALLBACK = (
    "Les informations disponibles ne permettent pas de répondre "
    "précisément à cette question."
)


def decision_process(intent, session_id=None, confidence=1.0, user_message=""):
    # Le DM est un FALLBACK purement technique et neutre.
    # Il ne produit AUCUNE réponse métier dérivée de l'intention BERT,
    # ne pose AUCUNE question et ne propose AUCUNE action.
    return {
        "response": NEUTRAL_FALLBACK,
        "service": "assistant",
        "is_fallback": True,
    }
