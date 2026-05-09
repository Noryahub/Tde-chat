from backend.app.services.conversation_service import save_conversation, get_session_history
from backend.app.dialogue.dialogue_manager import decision_process
from backend.app.responses.response_generator import get_response_from_db
from nlu.intent import process_predict
from backend.app.memory.memory_store import get_memory
from backend.app.rag.retriever import retrieve
from backend.app.llm.prompt_builder import build_prompt
from backend.app.llm.groq_client import generate_response


def process_message(user_message, session_id, user_id):

    # 1. Mémoire — init ou reconstruction depuis DB
    memory = get_memory(session_id)
    if len(memory.history) == 0:
        db_history = get_session_history(session_id)
        if db_history:
            memory.load_from_db(db_history)

    # 2. Vérifier si on attend un follow-up (ex: "oui" après une question du bot)
    awaiting_state = memory.get_context().get("awaiting_state")
    if awaiting_state:
        decision = decision_process(
            intent=None,
            session_id=session_id,
            confidence=1.0,
            user_message=user_message
        )
        bot_response = decision.get("response", "Je n'ai pas compris.")
        service = decision.get("service", "inconnu")
        memory.add_user_turn(content=user_message)
        memory.add_bot_turn(content=bot_response)
        save_conversation(user_id, session_id, user_message, "followup", 1.0, service, bot_response)
        return bot_response

    # 3. BERT — classification d'intention
    prediction = process_predict(user_message)
    intent = prediction["intent"]
    confidence = prediction["confidence"]
    print("INTENT RECU :", intent)
    print("CONFIDENCE :", confidence)

    memory.add_user_turn(content=user_message, intent=intent, confidence=confidence)

    # 4. RAG + LLM — réponse principale
    bot_response = None
    service = "service_client"

    try:
        retrieved_docs = retrieve(user_message, top_k=3)
        print(f"RAG : {len(retrieved_docs)} docs trouvés")

        if retrieved_docs:
            history_text = memory.get_history_as_text()
            prompt = build_prompt(user_message, intent, retrieved_docs, history_text)
            bot_response = generate_response(prompt)
            if bot_response:
                print("Groq : réponse générée ✅")

    except Exception as e:
        print(f"Erreur RAG/LLM : {e}")

    # 5. Fallback — si RAG/LLM échoue
    if not bot_response:
        print("→ Fallback Dialogue Manager")
        try:
            decision = get_response_from_db(intent, confidence)
        except:
            decision = None

        if not decision:
            decision = decision_process(
                intent,
                session_id=session_id,
                confidence=confidence,
                user_message=user_message
            )

        bot_response = decision.get("response", "Je n'ai pas compris votre demande.")
        service = decision.get("service", "inconnu")

    # 6. Sauvegardes
    memory.add_bot_turn(content=bot_response)
    save_conversation(user_id, session_id, user_message, intent, confidence, service, bot_response)

    return bot_response