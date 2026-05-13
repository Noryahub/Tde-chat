def build_prompt(user_message: str, intent: str, retrieved_docs: list,
                 history: str = "", session_context: dict = {}) -> str:

    context = "\n\n".join([
        f"Source : {doc['source']}\n{doc['text']}"
        for doc in retrieved_docs
    ])

    history_block = f"\nHistorique de la conversation :\n{history}\n" if history else ""

    # Contexte session — entités mémorisées
    context_block = ""
    if session_context:
        parts = []
        if session_context.get("localisation"):
            parts.append(f"Zone concernée : {session_context['localisation']}")
        if session_context.get("probleme"):
            parts.append(f"Problème en cours : {session_context['probleme']}")
        if parts:
            context_block = f"""
Contexte actuel de la conversation (informations déjà connues) :
{chr(10).join(parts)}
Toutes les questions suivantes sont relatives à ce contexte.
"""

    is_first_message = not history

    prompt = f"""Tu es un assistant virtuel de la Société Togolaise des Eaux (TdE).
Tu réponds uniquement aux questions liées aux services TDE : branchement, facturation, abonnement, réclamations, tarifs.
Tu réponds toujours en français, de manière claire, précise et professionnelle.

RÈGLES STRICTES :
- Fournis uniquement les informations présentes dans le contexte documentaire
- Si une information n'est pas dans le contexte, dis honnêtement que tu ne sais pas
- N'invente jamais de coordonnées, délais ou montants non mentionnés dans le contexte
- Si le contexte contient un numéro de téléphone ou email, tu peux le mentionner
{"- Présente-toi brièvement en début de réponse." if is_first_message else "- Ne te réintroduis pas, réponds directement à la question."}
{context_block}{history_block}
Contexte extrait du site TDE :
{context}

Question du client ({intent}) : {user_message}

Réponse :"""

    return prompt