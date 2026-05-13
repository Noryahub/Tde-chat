# Mapping intent → service TDE
INTENT_SERVICE_MAP = {
    "signaler_probleme":      "service_technique",
    "eligibilite_branchement":"service_technique",
    "demande_branchement":    "service_technique",
    "info_branchement":       "service_technique",
    "suivi_branchement":      "service_technique",
    "zone_couverture":        "service_client",
    "gestion_facture":        "service_commercial",
    "info_tarif":             "service_commercial",
    "demande_documents":      "service_commercial",
    "gestion_abonnement":     "service_client",
    "contact_service_client": "service_client",
    "horaire_agence":         "service_client",
    "info_generale":          "information",
    "info_consommation":      "information",
    "conseil_consommation":   "conseil",
    "fallback":               "assistant",
}

# Infos de contact par service
SERVICE_CONTACT = {
    "service_technique": {
        "nom": "Service Technique",
        "description": "Branchements, pannes, fuites, travaux",
        "horaires": "Lundi–Vendredi 7h30–16h00",
    },
    "service_commercial": {
        "nom": "Service Commercial",
        "description": "Factures, tarifs, abonnements, documents",
        "horaires": "Lundi–Vendredi 7h30–16h00",
    },
    "service_client": {
        "nom": "Service Client",
        "description": "Réclamations, informations générales, agences",
        "horaires": "Lundi–Vendredi 7h30–16h00",
    },
    "information": {
        "nom": "Information Générale",
        "description": "Renseignements sur la TDE et ses services",
        "horaires": "Disponible via le chatbot 24h/24",
    },
    "conseil": {
        "nom": "Conseil Consommation",
        "description": "Conseils sur la gestion de l'eau",
        "horaires": "Disponible via le chatbot 24h/24",
    },
    "assistant": {
        "nom": "Assistant Virtuel",
        "description": "Aide générale et reformulation",
        "horaires": "Disponible 24h/24",
    },
}

# Catégories de problèmes techniques reconnus
PROBLEME_MAP = {
    "fuite":    ["fuite", "coule", "écoulement", "fuites"],
    "coupure":  ["coupure", "coupé", "plus d'eau", "pas d'eau", "manque"],
    "pression": ["pression", "faible", "filet", "débit"],
    "eau sale": ["sale", "trouble", "couleur", "odeur", "marron"],
    "tuyau":    ["tuyau", "tuyeau", "canalisation", "conduite", "cassé", "percé"],
    "compteur": ["compteur", "relevé", "index"],
}


def get_service(intent: str) -> str:
    """Retourne le service compétent pour un intent donné."""
    return INTENT_SERVICE_MAP.get(intent, "service_client")


def get_service_info(intent: str) -> dict:
    """Retourne les infos complètes du service compétent."""
    service = get_service(intent)
    info = SERVICE_CONTACT.get(service, {})
    return {
        "service": service,
        "nom": info.get("nom", "Service Client"),
        "description": info.get("description", ""),
        "horaires": info.get("horaires", ""),
    }


def get_orientation_message(intent: str) -> str:
    """Génère un message d'orientation vers le bon service."""
    info = get_service_info(intent)
    return (
        f"Pour votre demande, je vous oriente vers notre "
        f"**{info['nom']}**. "
        f"{info['description']}. "
        f"Horaires : {info['horaires']}."
    )


def normalize_probleme(probleme: str) -> str:
    if not probleme:
        return None

    probleme_lower = probleme.lower()
    for categorie, mots_cles in PROBLEME_MAP.items():
        if any(mot in probleme_lower for mot in mots_cles):
            return categorie

    print(f"NER PROBLEME ignoré (hors catégories) : {probleme}")
    return None