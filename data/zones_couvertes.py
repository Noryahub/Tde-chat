# backend/app/data/zones_couvertes.py

ZONES_COUVERTES = {
    "lomé", "lome", "adidogomé", "adidogome", "tokoin",
    "agoè", "agoe", "tsévié", "tsevie", "kara",
    "sokodé", "sokode", "dapaong", "atakpamé", "atakpame",
    "kpalimé", "kpalime", "notsé", "notse",
}

ZONES_NON_COUVERTES = {
    # add zones you know are not covered
}


def check_coverage(localisation: str) -> str:
    """
    Returns:
        'couvert'       – zone is in the TDE network
        'non_couvert'   – zone is explicitly outside the network
        'inconnu'       – zone not recognised (let RAG handle it)
    """
    if not localisation:
        return "inconnu"

    loc = localisation.lower().strip()

    if loc in ZONES_COUVERTES:
        return "couvert"
    if loc in ZONES_NON_COUVERTES:
        return "non_couvert"
    return "inconnu"