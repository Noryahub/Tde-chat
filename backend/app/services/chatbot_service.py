from backend.app.services.conversation_service import save_conversation, get_session_history
from nlp.preprocess import process_nlp
from backend.app.dialogue.dialogue_manager import decision_process
#from backend.app.models.model_loader import process_predict
from backend.app.responses.response_generator import get_response_from_db
from nlu.intent import process_predict
from backend.app.memory.memory_store import get_memory
def process_message(user_message, session_id, user_id):

    # 0. Récupération / init mémoire de la session
    memory = get_memory(session_id)

    # Si mémoire vide (première fois ou après redémarrage serveur)
    #reconstruire depuis la DB
    if len(memory.history) == 0:
        db_history = get_session_history(session_id)             # ← nouveau
        if db_history:
            memory.load_from_db(db_history)

    # 1. NLP (ton code inchangé)
    clean_message = user_message

    # 2. Prédiction (ton code inchangé)
    prediction = process_predict(clean_message)
    intent = prediction["intent"]
    confidence = prediction["confidence"]

    print("INTENT RECU :", intent)
    print("CONFIDENCE :", confidence)

    # 3. Sauvegarder le tour utilisateur en mémoire RAM               ← nouveau
    memory.add_user_turn(content=user_message, intent=intent, confidence=confidence)

    # 4. Récupération réponse DB (ton code inchangé)
    try:
        decision = get_response_from_db(intent, confidence)
    except Exception as e:
        print("Erreur DB:", e)
        decision = None

    # 5. Fallback (ton code inchangé)
    if not decision:
        decision = decision_process(intent, confidence=confidence)

    bot_response = decision.get("response", "Je n'ai pas compris votre demande.")
    service = decision.get("service", "inconnu")

    # 6. Sauvegarder la réponse bot en mémoire RAM                    ← nouveau
    memory.add_bot_turn(content=bot_response)

    # 7. Sauvegarde DB (ton code inchangé)
    save_conversation(
        user_id,
        session_id,
        user_message,
        intent,
        confidence,
        service,
        bot_response
    )

    return bot_response