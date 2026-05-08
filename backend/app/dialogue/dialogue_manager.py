def decision_process(intent, text=None, confidence=1.0):
    # fallback si faible confiance
    print("INTENT RECU :", intent)
    print("CONFIDENCE :", confidence)
    if confidence < 0.01:
        return {
            "response": "Je ne suis pas sûr d’avoir compris votre demande. Pouvez-vous reformuler ?",
            "service": "inconnu"
        }


    responses = {

        "signaler_probleme": {
            "response": "Pouvez-vous préciser le problème rencontré ? Par exemple : coupure d’eau, fuite, eau sale ou faible pression.",
            "service": "service_technique"
        },

        "LABEL_11": {
            "response": "La TDE est chargée de la production et de la distribution d’eau potable au Togo.",
            "service": "information"
        },

        "info_tarif": {
            "response": "Les tarifs de l’eau varient selon la consommation et le type d’abonnement. Voulez-vous une estimation de facture ?",
            "service": "service_commercial"
        },

        "demande_branchement": {
            "response": "Pour obtenir un branchement d’eau, vous devez déposer une demande auprès de la TDE. Voulez-vous connaître les étapes ou les documents nécessaires ?",
            "service": "service_technique"
        },

        "contact_service_client": {
            "response": "Vous pouvez contacter le service client de la TDE par téléphone, en agence ou via leurs canaux officiels.",
            "service": "service_client"
        },

        "demande_documents": {
            "response": "Les documents demandés dépendent du service souhaité. Pouvez-vous préciser : abonnement, branchement, résiliation ou réabonnement ?",
            "service": "service_commercial"
        },

        "zone_couverture": {
            "response": "La TDE dessert plusieurs zones au Togo. Veuillez préciser votre quartier ou votre ville pour vérifier la couverture.",
            "service": "service_client"
        },

        "gestion_facture": {
            "response": "Je peux vous aider concernant votre facture : compréhension, réclamation, estimation ou paiement. Que souhaitez-vous faire ?",
            "service": "service_commercial"
        },

        "horaire_agence": {
            "response": "Les agences TDE sont généralement ouvertes du lundi au vendredi de 7h30 à 16h.",
            "service": "service_client"
        },

        "conseil_consommation": {
            "response": "Pour réduire votre consommation d’eau, pensez à réparer les fuites, fermer les robinets inutilisés et utiliser l’eau de manière rationnelle.",
            "service": "conseil"
        },

        "gestion_abonnement": {
            "response": "Je peux vous aider pour un abonnement, une modification, une résiliation ou un réabonnement. Que souhaitez-vous faire exactement ?",
            "service": "service_client"
        },

        "fallback": {
            "response": "Je ne suis pas sûr d’avoir compris votre demande. Pouvez-vous reformuler ou donner plus de détails ?",
            "service": "assistant"
        },

        "suivi_branchement": {
            "response": "Pour suivre l’évolution de votre demande de branchement, veuillez vous rapprocher de l’agence où le dossier a été déposé.",
            "service": "service_technique"
        },

        "info_consommation": {
            "response": "Une famille consomme en moyenne entre 10 et 20 m³ d’eau par mois selon les usages.",
            "service": "information"
        },

        "eligibilite_branchement": {
            "response": "L’éligibilité au branchement dépend de votre zone d’habitation. Pouvez-vous préciser votre quartier ?",
            "service": "service_technique"
        },

        "info_branchement": {
            "response": "Le branchement d’eau comprend généralement le dépôt du dossier, l’étude technique puis l’installation du compteur.",
            "service": "service_technique"
        }

    }

    return responses.get(intent, {
        "response": "Je n’ai pas bien compris votre demande. Pouvez-vous reformuler ?",
        "service": "inconnu"
    })