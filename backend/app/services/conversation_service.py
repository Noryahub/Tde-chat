from backend.app.database.db import get_db_connection

#historique ds conversations de l utiliateur

def get_user_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        SELECT
            user_message,
            bot_response,
            predicted_intent,
            confidence_score,
            orientation_service,
            created_at
        FROM conversations
        WHERE user_id = %s
        ORDER BY created_at DESC
         """
        cursor.execute(query, (user_id,))
        user_history = cursor.fetchall()

        history = []
        for row in user_history:
            history.append({
                "user_message": row[0],
                "bot_response": row[1],
                "predicted_intent": row[2],
                "confidence_score": row[3],
                "orientation_service": row[4],
                "created_at": row[5],
            })
        return history
    finally:
        cursor.close()
        conn.close()

def save_conversation(
    user_id,
    session_id,
    user_message,
    intent,
    confidence,
    service,
    bot_response
):

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO conversations (
            user_id,
            session_id,
            user_message,
            bot_response,
            predicted_intent,
            confidence_score,
            orientation_service
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            user_id,
            session_id,
            user_message,
            bot_response,
            intent,
            confidence,
            service
        )

        cursor.execute(query, values)
        conn.commit()

    except Exception as e:
        print("Erreur lors de l'enregistrement :", e)

    finally:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.close()
        conn.close()

