def build_prompt(user_message: str, intent: str, retrieved_docs: list, history: str = "") -> str:
    context = "\n\n".join([
        f"Source : {doc['source']}\n{doc['text']}"
        for doc in retrieved_docs
    ])

    history_block = f"\nHistorique de la conversation :\n{history}\n" if history else ""

    prompt = f"""Tu es un assistant virtuel de la Société Togolaise des Eaux (TdE).
Tu réponds uniquement aux questions liées aux services TDE : branchement, facturation, abonnement, réclamations, tarifs.
Tu réponds toujours en français, de manière claire, précise et professionnelle.
Si l'information n'est pas dans le contexte fourni, dis-le honnêtement.
{history_block}
Contexte extrait du site TDE :
{context}

Question du client ({intent}) : {user_message}

Réponse :"""

    return prompt