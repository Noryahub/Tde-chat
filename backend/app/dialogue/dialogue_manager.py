# backend/app/dialogue/dialogue_manager.py

from backend.app.memory.memory_store import get_memory

CONFIDENCE_THRESHOLD = 0.01

# Intents qui nécessitent une localisation pour répondre précisément
INTENTS_NEED_LOCATION = {
    "signaler_probleme",
    "eligibilite_branchement",
    "zone_couverture"
}

# Intents qui nécessitent un numéro client
INTENTS_NEED_CLIENT = {
    "gestion_facture",
    "gestion_abonnement",
    "suivi_branchement"
}

# Réponses métier
RESPONSES = {
    "conseil_consommation": {
        "response": "Pour réduire votre consommation, pensez à réparer les fuites, fermer les robinets inutilisés et utiliser l'eau rationnellement.",
        "service": "conseil"
    },
    "contact_service_client": {
        "response": "Vous pouvez contacter le service client TDE par téléphone, en agence ou via leurs canaux officiels.",
        "service": "service_client"
    },
    "demande_branchement": {
        "response": "Pour un branchement d'eau, vous devez déposer une demande auprès de la TDE. Voulez-vous connaître les étapes ou les documents nécessaires ?",
        "service": "service_technique"
    },
    "demande_documents": {
        "response": "Les documents dépendent du service souhaité. Précisez : abonnement, branchement, résiliation ou réabonnement ?",
        "service": "service_commercial"
    },
    "eligibilite_branchement": {
        "response": "L'éligibilité au branchement dépend de votre zone. Pouvez-vous préciser votre quartier ou ville ?",
        "service": "service_technique"
    },
    "fallback": {
        "response": "Je ne suis pas sûr d'avoir compris. Pouvez-vous reformuler ou donner plus de détails ?",
        "service": "assistant"
    },
    "gestion_abonnement": {
        "response": "Je peux vous aider pour un abonnement, une modification, une résiliation ou un réabonnement. Que souhaitez-vous faire ?",
        "service": "service_client"
    },
    "gestion_facture": {
        "response": "Je peux vous aider concernant votre facture : compréhension, réclamation, estimation ou paiement. Que souhaitez-vous faire ?",
        "service": "service_commercial"
    },
    "horaire_agence": {
        "response": "Les agences TDE sont ouvertes du lundi au vendredi de 7h30 à 16h.",
        "service": "service_client"
    },
    "info_branchement": {
        "response": "Le branchement comprend : dépôt du dossier, étude technique puis installation du compteur.",
        "service": "service_technique"
    },
    "info_consommation": {
        "response": "Une famille consomme en moyenne entre 10 et 20 m³ d'eau par mois selon les usages.",
        "service": "information"
    },
    "info_generale": {
        "response": "La TDE est chargée de la production et de la distribution d'eau potable au Togo.",
        "service": "information"
    },
    "info_tarif": {
        "response": "Les tarifs varient selon la consommation et le type d'abonnement. Voulez-vous une estimation de facture ?",
        "service": "service_commercial"
    },
    "signaler_probleme": {
        "response": "Pouvez-vous préciser le problème ? Par exemple : coupure d'eau, fuite, eau sale ou faible pression.",
        "service": "service_technique"
    },
    "suivi_branchement": {
        "response": "Pour suivre votre demande de branchement, rapprochez-vous de l'agence où le dossier a été déposé.",
        "service": "service_technique"
    },
    "zone_couverture": {
        "response": "La TDE dessert plusieurs zones au Togo. Précisez votre quartier ou ville pour vérifier la couverture.",
        "service": "service_client"
    },
}


def decision_process(intent, session_id=None, confidence=1.0):
    print("INTENT RECU :", intent)
    print("CONFIDENCE :", confidence)

    # 1. Confiance trop faible → fallback immédiat
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "response": "Je ne suis pas sûr d'avoir compris votre demande. Pouvez-vous reformuler ?",
            "service": "inconnu"
        }

    # 2. Intent explicitement fallback
    if intent == "fallback":
        return RESPONSES["fallback"]

    # 3. Récupérer le contexte de session si disponible
    session_context = {}
    if session_id:
        memory = get_memory(session_id)
        session_context = memory.get_context()

    # 4. Intents nécessitant une localisation
    if intent in INTENTS_NEED_LOCATION:
        localisation = session_context.get("localisation")
        if not localisation:
            return {
                "response": "Pour mieux vous aider, pouvez-vous préciser votre quartier ou votre ville ?",
                "service": RESPONSES.get(intent, {}).get("service", "service_technique")
            }

    # 5. Intents nécessitant un numéro client
    if intent in INTENTS_NEED_CLIENT:
        numero_client = session_context.get("numero_client")
        if not numero_client:
            return {
                "response": "Pour traiter votre demande, pouvez-vous me communiquer votre numéro client ou numéro de compteur ?",
                "service": RESPONSES.get(intent, {}).get("service", "service_commercial")
            }

    # 6. Réponse normale
    return RESPONSES.get(intent, {
        "response": "Je n'ai pas bien compris votre demande. Pouvez-vous reformuler ?",
        "service": "inconnu"
    })