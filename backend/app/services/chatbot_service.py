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
from backend.app.services.orientation_service import get_service, get_service_info, normalize_probleme
from backend.app.constants.ticket_intents import (
    TICKET_INTENTS
)
from backend.app.repositories.ticket_repository import create_ticket
from backend.app.utils.ticket_generator import (
    generate_ticket_number
)


def process_message(user_message, session_id, user_id,  conversation_id=None):

    # 1. Mémoire — init ou reconstruction depuis DB
    memory = get_memory(session_id)
    print("CTX =", memory.get_context())
    #context
    ctx = memory.get_context()
    ticket_step = ctx.get("ticket_step")
    if ticket_step == "telephone":
        memory.update_context({
            "telephone": user_message,
            "ticket_step": "localisation"
        })

        return {
            "response":
                "Merci. Quelle est votre localisation ?",
            "intent": "ticket_creation",
            "ticket_proposal": False
        }
    if ticket_step == "localisation":
        memory.update_context({
            "ticket_localisation": user_message,
            "ticket_step": "description"
        })

        return {
            "response":
                "Merci. Décrivez brièvement votre problème.",
            "intent": "ticket_creation",
            "ticket_proposal": False
        }
    if ticket_step == "description":
        telephone = ctx.get("telephone")
        localisation = ctx.get("ticket_localisation")
        description = user_message

        ticket_number = generate_ticket_number()

        create_ticket(
            ticket_number=ticket_number,
            nom=None,
            email=None,
            telephone=telephone,
            localisation=localisation,
            description=description,
            intent=ctx.get("probleme")
        )

        memory.clear_ticket_context()

        return {
            "response":
                f"Votre ticket {ticket_number} a bien été créé. Nos équipes reviendront vers vous dans les meilleurs délais.",
            "intent": "ticket_created",
            "ticket_proposal": False
        }
    user_lower = user_message.lower().strip()
    if (
            ctx.get("ticket_proposal")
            and user_lower in [
        "oui",
        "ok",
        "yes",
        "d'accord"
    ]
    ):
        memory.update_context({
            "ticket_proposal": False,
            "ticket_step": "telephone"
        })

        return {
            "response":
                "Très bien. Veuillez renseigner votre numéro de téléphone.",
            "intent": "ticket_creation",
            "ticket_proposal": False
        }
    if (
            ctx.get("ticket_proposal")
            and user_lower in [
        "non",
        "no"
    ]
    ):
        memory.update_context({
            "ticket_proposal": False
        })

        return {
            "response":
                "Très bien. N'hésitez pas à revenir vers moi si vous avez besoin d'assistance.",
            "intent": "ticket_refused",
            "ticket_proposal": False
        }
    if len(memory.history) == 0:
        db_history = get_session_history(session_id)
        if db_history:
            memory.load_from_db(db_history)

    # 2. NER — extraction des entités dès le début
    entities = extract_entities(user_message)
    localisation_detected = entities.get("localisation") or None
    probleme_detected = normalize_probleme(entities.get("probleme")) or None

    # Mise à jour mémoire uniquement si détecté
    if localisation_detected:
        memory.update_context({"localisation": localisation_detected})
    if probleme_detected:
        memory.update_context({"probleme": probleme_detected})

    # 3. BERT — classification d'intention
    prediction = process_predict(user_message)
    intent = prediction["intent"]
    confidence = prediction["confidence"]
    print("INTENT RECU :", intent)
    print("CONFIDENCE :", confidence)
    memory.add_user_turn(content=user_message, intent=intent, confidence=confidence)

    # 4. RAG + LLM — réponse principale
    bot_response = None
    service = get_service(intent)
    print(f"SERVICE : {service}")

    try:
        retrieved_docs = retrieve(user_message, top_k=3)
        print(f"RAG : {len(retrieved_docs)} docs trouvés")

        if retrieved_docs:
            history_text = memory.get_history_as_text()
            session_ctx = memory.get_context()
            prompt = build_prompt(user_message, intent, retrieved_docs, history_text, session_context=session_ctx)
            raw_response = generate_response(prompt)

            if raw_response:
                validation = validate_response(raw_response, intent)
                if validation["valid"]:
                    bot_response = validation["response"]
                    print("Groq : réponse validée")
                else:
                    print(f"Groq : réponse rejetée — {validation['reason']}")
                    bot_response = None

    except Exception as e:
        print(f"Erreur RAG/LLM : {e}")

    # 5. Fallback — si RAG/LLM échoue
    if not bot_response:
        print("→ Fallback Dialogue Manager")
        try:
            decision = get_response_from_db(intent, confidence)
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

    # 6. Sauvegarde — uniquement les entités du message courant
    memory.add_bot_turn(content=bot_response)
    conversation_id = save_conversation(
        user_id=user_id,
        conversation_id=conversation_id,
        session_id=session_id,
        user_message=user_message,
        intent=intent,
        confidence=confidence,
        service=service,
        bot_response=bot_response,
        localisation=localisation_detected,
        probleme=probleme_detected
    )
    # gestion des tickets
    ticket_proposal = (
            intent in TICKET_INTENTS
    )
    if ticket_proposal:
        memory.update_context({
            "ticket_proposal": True
        })
    return {
        "response": bot_response,
        "intent": intent,
        "conversation_id": conversation_id,
        "ticket_proposal": ticket_proposal,
    }