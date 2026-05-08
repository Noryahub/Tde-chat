from backend.app.database.db import get_db_connection

def get_response_from_db(intent, confidence, threshold=0.01):

    # fallback si faible confiance
    if confidence < threshold:
        return {
            "response": "Je ne suis pas sûr d’avoir compris votre demande. Pouvez-vous reformuler ?",
            "service": None
        }

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  #important

    query = "SELECT response, service FROM responses WHERE intent = %s LIMIT 1"
    cursor.execute(query, (intent,))  #passer le paramètre

    result = cursor.fetchone()  #récupérer une ligne

    cursor.close()
    conn.close()

    if result:
        return {
            "response": result["response"],
            "service": result["service"]
        }

    # fallback si aucune réponse trouvée
    return {
        "response": "Je n’ai pas encore d’information pour cette demande. Veuillez contacter une agence TDE.",
        "service": "service_client"
    }