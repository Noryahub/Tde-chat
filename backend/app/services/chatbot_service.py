from backend.app.services.conversation_service import save_conversation, get_session_history
from backend.app.dialogue.dialogue_manager import decision_process
from backend.app.responses.response_generator import get_response_from_db
from nlu.intent import process_predict
from nlu.ner import extract_entities
from backend.app.memory.memory_store import get_memory
from backend.app.rag.retriever import retrieve
from backend.app.llm.prompt_builder import build_prompt
from backend.app.llm.groq_client import generate_response
from backend.app.validation.response_validator import validate_response
from backend.app.services.orientation_service import get_service, get_service_info


def process_message(user_message, session_id, user_id):

    # 1. Mémoire — init ou reconstruction depuis DB
    memory = get_memory(session_id)
    if len(memory.history) == 0:
        db_history = get_session_history(session_id)
        if db_history:
            memory.load_from_db(db_history)

    # 2. NER — extraction des entités dès le début
    entities = extract_entities(user_message)

    # Capture directe des entités détectées pour CE message (None si rien détecté)
    localisation_detected = entities.get("localisation") or None
    probleme_detected = entities.get("probleme") or None

    # Mise à jour mémoire uniquement si détecté
    if localisation_detected:
        memory.update_context({"localisation": localisation_detected})
    if probleme_detected:
        memory.update_context({"probleme": probleme_detected})

    # 3. Vérifier si on attend un follow-up
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

        # Priorité aux entités du message courant, fallback sur le contexte mémoire
        session_ctx = memory.get_context()
        save_conversation(
            user_id, session_id, user_message,
            "followup", 1.0, service, bot_response,
            localisation=localisation_detected or session_ctx.get("localisation"),
            probleme=probleme_detected or session_ctx.get("probleme")
        )
        return bot_response

    # 4. BERT — classification d'intention
    prediction = process_predict(user_message)
    intent = prediction["intent"]
    confidence = prediction["confidence"]
    print("INTENT RECU :", intent)
    print("CONFIDENCE :", confidence)
    memory.add_user_turn(content=user_message, intent=intent, confidence=confidence)

    # 5. RAG + LLM — réponse principale
    bot_response = None
    service = get_service(intent)
    print(f"SERVICE : {service}")
    try:
        retrieved_docs = retrieve(user_message, top_k=3)
        print(f"RAG : {len(retrieved_docs)} docs trouvés")

        if retrieved_docs:
            history_text = memory.get_history_as_text()
            prompt = build_prompt(user_message, intent, retrieved_docs, history_text)
            raw_response = generate_response(prompt)

            if raw_response:
                # Validation avant envoi
                validation = validate_response(raw_response, intent)
                if validation["valid"]:
                    bot_response = validation["response"]
                    print("Groq : réponse validée")
                else:
                    print(f"Groq : réponse rejetée — {validation['reason']}")
                    bot_response = None  # → fallback

    except Exception as e:
        print(f"Erreur RAG/LLM : {e}")

    # 6. Fallback — si RAG/LLM échoue
    if not bot_response:
        print("→ Fallback Dialogue Manager")
        try:
            decision = decision_process(
                intent, session_id=session_id,
                confidence=confidence, user_message=user_message
            )
        except Exception:
            decision = None

        if not decision:
            decision = decision_process(
                intent,
                session_id=session_id,
                confidence=confidence,
                user_message=user_message
            )

        bot_response = decision.get("response", "Je n'ai pas compris votre demande.")
        service = get_service(intent)

    # 7. Sauvegarde
    memory.add_bot_turn(content=bot_response)

    # Priorité aux entités du message courant, fallback sur le contexte mémoire
    session_ctx = memory.get_context()
    save_conversation(
        user_id, session_id, user_message,
        intent, confidence, service, bot_response,
        localisation=localisation_detected or session_ctx.get("localisation"),
        probleme=probleme_detected or session_ctx.get("probleme")
    )

    return bot_response