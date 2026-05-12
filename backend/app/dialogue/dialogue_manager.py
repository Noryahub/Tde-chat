from backend.app.memory.memory_store import get_memory
from data.zones_couvertes import check_coverage

CONFIDENCE_THRESHOLD = 0.4
MAX_CLARIFICATION_ATTEMPTS = 3

# Infos requises par intent
REQUIRED_INFO = {
    "eligibilite_branchement": ["localisation"],
    "signaler_probleme":       ["localisation", "probleme"],
    "zone_couverture":         ["localisation"],
    "suivi_branchement":       ["localisation"],
}

# Questions de clarification par champ manquant
QUESTIONS = {
    "localisation": {
        "first":   "Pour mieux vous aider, pouvez-vous préciser votre quartier ou votre ville ?",
        "retry":   "Je n'ai pas bien compris votre zone. Pouvez-vous préciser ? Ex : Lomé, Kara, Adidogomé, Tokoin...",
        "example": "Merci de préciser votre localisation parmi ces exemples : Lomé, Kara, Adidogomé, Tokoin, Agoè, Tsévié, Dapaong, Sokodé."
    },
    "probleme": {
        "first":   "Quel est le problème exact rencontré ?",
        "retry":   "Je n'ai pas bien identifié le problème. S'agit-il d'une fuite, d'une coupure, d'eau sale ou d'une faible pression ?",
        "example": "Pouvez-vous choisir parmi : fuite d'eau, coupure d'eau, eau sale/trouble, faible pression, tuyau cassé."
    }
}

# Stratégie de secours après MAX_CLARIFICATION_ATTEMPTS
FALLBACK_CLARIFICATION = {
    "localisation": (
        "Je n'arrive pas à identifier votre zone après plusieurs tentatives. "
        "Je vous invite à vous rapprocher directement de l'agence TDE la plus proche "
        "ou à utiliser le formulaire de réclamation sur tde.tg pour obtenir une assistance personnalisée."
    ),
    "probleme": (
        "Je n'arrive pas à identifier votre problème précisément. "
        "Veuillez contacter notre service technique directement à l'agence TDE "
        "ou décrire votre situation par écrit via le formulaire sur tde.tg."
    )
}

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
        "response": "L'éligibilité au branchement dépend de votre zone.",
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
        "response": "La TDE dessert plusieurs zones au Togo.",
        "service": "service_client"
    },
}

FOLLOWUP_KEYWORDS = {
    "awaiting_branchement_precision": {
        "etapes":    ["etape", "étape", "procedure", "procédure", "comment", "oui", "faire"],
        "documents": ["document", "dossier", "pièce", "piece", "fichier", "papier"]
    },
    "awaiting_abonnement_action": {
        "nouveau":      ["nouveau", "nouvel", "souscrire", "créer", "ouvrir"],
        "resiliation":  ["résilier", "resilier", "fermer", "annuler", "arrêter"],
        "modification": ["modifier", "changer", "mettre à jour", "actualiser"]
    },
    "awaiting_facture_action": {
        "paiement":    ["payer", "paiement", "régler", "money", "mobile"],
        "reclamation": ["contester", "réclamation", "erreur", "faux", "incorrect"],
        "comprendre":  ["comprendre", "explication", "détail", "lire", "signifie"]
    },
    "awaiting_documents_type": {
        "abonnement":  ["abonnement", "abonner", "souscrire"],
        "branchement": ["branchement", "brancher", "compteur"],
        "resiliation": ["résiliation", "résilier", "fermer"]
    }
}

FOLLOWUP_RESPONSES = {
    "awaiting_branchement_precision": {
        "etapes": {
            "response": "Les étapes sont :\n1. Retirer le formulaire à l'agence TDE\n2. Déposer le dossier complet\n3. Attendre l'étude technique\n4. Payer les frais\n5. Installation du compteur.",
            "service": "service_technique"
        },
        "documents": {
            "response": "Documents requis : pièce d'identité, titre de propriété ou bail, plan de localisation, formulaire TDE.",
            "service": "service_technique"
        },
        "ambigu": {
            "response": "Souhaitez-vous les étapes de la procédure ou la liste des documents nécessaires ?",
            "service": "service_technique"
        }
    },
    "awaiting_abonnement_action": {
        "nouveau": {
            "response": "Pour un nouvel abonnement : pièce d'identité, justificatif de domicile et formulaire TDE.",
            "service": "service_client"
        },
        "resiliation": {
            "response": "Pour résilier : contrat d'abonnement et pièce d'identité à l'agence TDE.",
            "service": "service_client"
        },
        "modification": {
            "response": "Pour modifier votre abonnement, contactez l'agence avec votre numéro client.",
            "service": "service_client"
        },
        "ambigu": {
            "response": "Précisez : nouvel abonnement, modification, résiliation ou réabonnement ?",
            "service": "service_client"
        }
    },
    "awaiting_facture_action": {
        "paiement": {
            "response": "Vous pouvez payer en agence TDE, par mobile money ou via les points agréés.",
            "service": "service_commercial"
        },
        "reclamation": {
            "response": "Pour contester une facture, rendez-vous à l'agence avec votre facture.",
            "service": "service_commercial"
        },
        "comprendre": {
            "response": "Votre facture TDE comprend : coût de consommation (m³), redevance fixe et taxes.",
            "service": "service_commercial"
        },
        "ambigu": {
            "response": "Que souhaitez-vous faire : payer, contester ou comprendre votre facture ?",
            "service": "service_commercial"
        }
    },
    "awaiting_documents_type": {
        "abonnement": {
            "response": "Pour un abonnement : pièce d'identité, justificatif de domicile, formulaire TDE.",
            "service": "service_commercial"
        },
        "branchement": {
            "response": "Pour un branchement : pièce d'identité, titre de propriété, plan de localisation, formulaire TDE.",
            "service": "service_commercial"
        },
        "resiliation": {
            "response": "Pour une résiliation : contrat, pièce d'identité, dernière facture réglée.",
            "service": "service_commercial"
        },
        "ambigu": {
            "response": "Précisez : abonnement, branchement, résiliation ou réabonnement ?",
            "service": "service_commercial"
        }
    }
}

AWAITING_TRIGGERS = {
    "demande_branchement": "awaiting_branchement_precision",
    "demande_documents":   "awaiting_documents_type",
    "gestion_abonnement":  "awaiting_abonnement_action",
    "gestion_facture":     "awaiting_facture_action",
}


def _get_clarification_question(field: str, attempts: int) -> str:
    """Retourne la question adaptée selon le nombre de tentatives."""
    questions = QUESTIONS.get(field, {})
    if attempts == 0:
        return questions.get("first", "Pouvez-vous préciser ?")
    elif attempts == 1:
        return questions.get("retry", "Je n'ai pas compris, pouvez-vous reformuler ?")
    else:
        return questions.get("example", "Pouvez-vous donner plus de détails ?")


def _get_missing_fields(intent: str, session_context: dict) -> list:
    """Retourne la liste des champs manquants pour un intent donné."""
    required = REQUIRED_INFO.get(intent, [])
    return [
        field for field in required
        if not session_context.get(field)
    ]


def _detect_followup_key(awaiting_state: str, user_message: str) -> str:
    msg = user_message.lower()
    keywords = FOLLOWUP_KEYWORDS.get(awaiting_state, {})
    for key, words in keywords.items():
        if any(w in msg for w in words):
            return key
    return "ambigu"


def _handle_followup(awaiting_state: str, user_message: str, memory) -> dict:
    key = _detect_followup_key(awaiting_state, user_message)
    responses = FOLLOWUP_RESPONSES.get(awaiting_state, {})
    result = responses.get(key, responses.get("ambigu"))
    if key != "ambigu":
        memory.update_context({"awaiting_state": None})
    return result


def _handle_eligibilite(localisation: str) -> dict:
    """Vérifie la couverture et retourne la réponse d'éligibilité."""
    coverage = check_coverage(localisation)
    if coverage == "couvert":
        return {
            "response": (
                f"Votre zone à {localisation} est couverte par le réseau TDE. "
                f"Vous pouvez effectuer une demande de branchement. "
                f"Souhaitez-vous connaître les documents nécessaires ?"
            ),
            "service": "service_technique"
        }
    elif coverage == "non_couvert":
        return {
            "response": (
                f"Malheureusement, votre zone à {localisation} n'est pas encore "
                f"couverte par le réseau TDE. Contactez l'agence la plus proche "
                f"pour plus d'informations."
            ),
            "service": "service_technique"
        }
    else:
        return None  # Zone inconnue → laisser le RAG répondre


def decision_process(intent, session_id=None, confidence=1.0, user_message=""):
    print("DIALOGUE MANAGER — intent:", intent, "| confidence:", confidence)

    session_context = {}
    memory = None

    if session_id:
        memory = get_memory(session_id)
        session_context = memory.get_context()

    awaiting_state = session_context.get("awaiting_state")

    # 1. Follow-up simple en attente (branchement, documents, facture, abonnement)
    if awaiting_state and awaiting_state in FOLLOWUP_RESPONSES and memory:
        return _handle_followup(awaiting_state, user_message, memory)

    # 2. Intent None, fallback ou confidence faible
    if not intent or intent == "fallback" or confidence < CONFIDENCE_THRESHOLD:
        return RESPONSES["fallback"]

    # 3. Vérifier les infos manquantes pour cet intent
    missing_fields = _get_missing_fields(intent, session_context)

    if missing_fields:
        field = missing_fields[0]  # traiter un champ à la fois

        # Récupérer le compteur de tentatives
        attempt_key = f"attempts_{field}"
        attempts = session_context.get(attempt_key, 0)

        # Stratégie de secours si trop de tentatives
        if attempts >= MAX_CLARIFICATION_ATTEMPTS:
            # Réinitialiser le compteur et l'awaiting_state
            if memory:
                memory.update_context({
                    attempt_key: 0,
                    "awaiting_state": None
                })
            return {
                "response": FALLBACK_CLARIFICATION.get(
                    field,
                    "Je vous invite à contacter directement une agence TDE."
                ),
                "service": "service_client"
            }

        # Incrémenter le compteur et poser la question
        if memory:
            memory.update_context({
                attempt_key: attempts + 1,
                "awaiting_state": f"awaiting_{field}"
            })

        question = _get_clarification_question(field, attempts)
        return {
            "response": question,
            "service": RESPONSES.get(intent, {}).get("service", "service_client")
        }

    # 4. Toutes les infos disponibles — logique métier
    if intent == "eligibilite_branchement":
        result = _handle_eligibilite(session_context.get("localisation"))
        if result:
            # Réinitialiser les compteurs
            if memory:
                memory.update_context({
                    "attempts_localisation": 0,
                    "awaiting_state": None
                })
            return result

    # 5. Déclencher awaiting_state si nécessaire
    if intent in AWAITING_TRIGGERS and memory:
        memory.update_context({"awaiting_state": AWAITING_TRIGGERS[intent]})

    # 6. Réponse normale
    return RESPONSES.get(intent, {
        "response": "Je n'ai pas bien compris votre demande. Pouvez-vous reformuler ?",
        "service": "inconnu"
    })