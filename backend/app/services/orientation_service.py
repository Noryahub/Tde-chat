
INTENT_SERVICE_MAP = {
    "signaler_probleme":       "service_technique",
    "eligibilite_branchement": "service_technique",
    "demande_branchement":     "service_technique",
    "info_branchement":        "service_technique",
    "suivi_branchement":       "service_technique",

    "zone_couverture":         "service_client",

    "gestion_facture":         "service_commercial",
    "info_tarif":              "service_commercial",
    "demande_documents":       "service_commercial",

    "gestion_abonnement":      "service_client",
    "contact_service_client":  "service_client",
    "horaire_agence":          "service_client",

    "info_generale":           "information",
    "info_consommation":       "information",

    "conseil_consommation":    "conseil",

    "fallback":                "assistant",
}

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

PROBLEME_MAP = {

    "fuite": [
        "fuite",
        "coule",
        "écoulement",
        "ecoulement",
        "fuites"
    ],

    "coupure": [
        "coupure",
        "coupé",
        "coupe",
        "plus d'eau",
        "pas d'eau",
        "manque d'eau",
        "absence d'eau"
    ],

    "pression": [
        "pression",
        "faible pression",
        "débit",
        "debit",
        "filet d'eau"
    ],

    "eau sale": [
        "sale",
        "trouble",
        "marron",
        "odeur",
        "couleur"
    ],

    "tuyau": [
        "tuyau",
        "canalisation",
        "conduite",
        "cassé",
        "casse",
        "percé",
        "perce"
    ],

    "compteur": [
        "compteur",
        "relevé",
        "releve",
        "index"
    ],

    "branchement": [
        "branchement",
        "brancher",
        "raccordement"
    ]
}



def get_service(intent: str) -> str:
    return INTENT_SERVICE_MAP.get(intent, "service_client")

def get_service_info(intent: str) -> dict:
    service = get_service(intent)
    info = SERVICE_CONTACT.get(service, {})
    return {
        "service": service,
        "nom": info.get("nom", "Service Client"),
        "description": info.get("description", ""),
        "horaires": info.get("horaires", ""),
    }


def get_orientation_message(intent: str) -> str:
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

    probleme_lower = probleme.lower().strip()

    # Recherche correspondance métier
    for categorie, mots_cles in PROBLEME_MAP.items():

        if any(mot in probleme_lower for mot in mots_cles):

            print(f"PROBLEME NORMALISE : {probleme} -> {categorie}")

            return categorie

    # Rejet des faux positifs NER
    print(f"PROBLEME REJETE : {probleme}")

    return None