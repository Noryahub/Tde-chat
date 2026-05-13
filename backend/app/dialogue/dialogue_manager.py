from backend.app.memory.memory_store import get_memory
from data.zones_couvertes import check_coverage

CONFIDENCE_THRESHOLD = 0.4

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
        "response": "Pour un branchement d'eau, vous devez déposer une demande auprès de la TDE.",
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
        "response": "Votre signalement a bien été enregistré. Notre service technique en sera informé.",
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


def decision_process(intent, session_id=None, confidence=1.0, user_message=""):
    print("DIALOGUE MANAGER — intent:", intent, "| confidence:", confidence)

    session_context = {}
    memory = None

    if session_id:
        memory = get_memory(session_id)
        session_context = memory.get_context()

    # 1. Intent None, fallback ou confidence faible
    if not intent or intent == "fallback" or confidence < CONFIDENCE_THRESHOLD:
        return RESPONSES["fallback"]

    # 2. Eligibilité branchement — vérification couverture si localisation connue
    if intent == "eligibilite_branchement":
        localisation = session_context.get("localisation")
        if localisation:
            coverage = check_coverage(localisation)
            if coverage == "couvert":
                return {
                    "response": f"Votre zone à {localisation} est couverte par le réseau TDE. Vous pouvez effectuer une demande de branchement. Souhaitez-vous connaître les documents nécessaires ?",
                    "service": "service_technique"
                }
            elif coverage == "non_couvert":
                return {
                    "response": f"Malheureusement, votre zone à {localisation} n'est pas encore couverte par le réseau TDE. Contactez l'agence la plus proche pour plus d'informations.",
                    "service": "service_technique"
                }
            return None  # Zone inconnue → RAG répond

    # 3. Réponse normale
    return RESPONSES.get(intent, {
        "response": "Je n'ai pas bien compris votre demande. Pouvez-vous reformuler ?",
        "service": "inconnu"
    })