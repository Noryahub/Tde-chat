from backend.app.database.db import get_db_connection


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
            localisation,
            probleme,
            created_at
        FROM conversations
        WHERE user_id = %s
        ORDER BY created_at DESC
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        history = []
        for row in rows:
            history.append({
                "user_message": row[0],
                "bot_response": row[1],
                "predicted_intent": row[2],
                "confidence_score": row[3],
                "orientation_service": row[4],
                "localisation": row[5],
                "probleme": row[6],
                "created_at": row[7],
            })
        return history

    finally:
        cursor.close()
        conn.close()


def get_session_history(session_id, limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        SELECT
            user_message,
            bot_response,
            predicted_intent,
            confidence_score
        FROM conversations
        WHERE session_id = %s
        ORDER BY created_at DESC
        LIMIT %s
        """
        cursor.execute(query, (session_id, limit))
        rows = cursor.fetchall()

        history = []
        for row in reversed(rows):
            history.append({
                "user_message": row[0],
                "bot_response": row[1],
                "intent": row[2],
                "confidence": row[3],
            })
        return history

    except Exception as e:
        print("Erreur récupération historique session :", e)
        return []

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
    bot_response,
    localisation=None,  # ← nouveau
    probleme=None       # ← nouveau
):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Sauvegarde conversation
        query = """
        INSERT INTO conversations (
            user_id,
            session_id,
            user_message,
            bot_response,
            predicted_intent,
            confidence_score,
            orientation_service,
            localisation,
            probleme
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_id,
            session_id,
            user_message,
            bot_response,
            intent,
            confidence,
            service,
            localisation,
            probleme
        )
        cursor.execute(query, values)
        conv_id = cursor.lastrowid

        # 2. Créer un signalement si problème détecté
        if intent == "signaler_probleme" and (localisation or probleme):
            cursor.execute("""
                INSERT INTO signalements (
                    conversation_id,
                    user_id,
                    session_id,
                    localisation,
                    probleme,
                    intent,
                    statut
                )
                VALUES (%s, %s, %s, %s, %s, %s, 'nouveau')
            """, (conv_id, user_id, session_id, localisation, probleme, intent))

        conn.commit()

    except Exception as e:
        print("Erreur lors de l'enregistrement :", e)

    finally:
        cursor.close()
        conn.close()


def get_signalements(statut=None, limit=50):
    """Récupère les signalements pour le dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if statut:
            query = """
            SELECT
                id, localisation, probleme,
                intent, statut, created_at
            FROM signalements
            WHERE statut = %s
            ORDER BY created_at DESC
            LIMIT %s
            """
            cursor.execute(query, (statut, limit))
        else:
            query = """
            SELECT
                id, localisation, probleme,
                intent, statut, created_at
            FROM signalements
            ORDER BY created_at DESC
            LIMIT %s
            """
            cursor.execute(query, (limit,))

        rows = cursor.fetchall()
        signalements = []
        for row in rows:
            signalements.append({
                "id": row[0],
                "localisation": row[1],
                "probleme": row[2],
                "intent": row[3],
                "statut": row[4],
                "created_at": row[5],
            })
        return signalements

    except Exception as e:
        print("Erreur récupération signalements :", e)
        return []

    finally:
        cursor.close()
        conn.close()


def get_analytics() -> dict:
    """Retourne les indicateurs analytiques pour le dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        analytics = {}

        # Total conversations
        cursor.execute("SELECT COUNT(*) FROM conversations")
        analytics["total_conversations"] = cursor.fetchone()[0]

        # Intent le plus fréquent
        cursor.execute("""
            SELECT predicted_intent, COUNT(*) as total
            FROM conversations
            WHERE predicted_intent IS NOT NULL
            GROUP BY predicted_intent
            ORDER BY total DESC
            LIMIT 5
        """)
        analytics["top_intents"] = [
            {"intent": row[0], "count": row[1]}
            for row in cursor.fetchall()
        ]

        # Zone la plus touchée
        cursor.execute("""
            SELECT localisation, COUNT(*) as total
            FROM conversations
            WHERE localisation IS NOT NULL
            GROUP BY localisation
            ORDER BY total DESC
            LIMIT 5
        """)
        analytics["top_localisations"] = [
            {"localisation": row[0], "count": row[1]}
            for row in cursor.fetchall()
        ]

        # Problèmes les plus fréquents
        cursor.execute("""
            SELECT probleme, COUNT(*) as total
            FROM conversations
            WHERE probleme IS NOT NULL
            GROUP BY probleme
            ORDER BY total DESC
            LIMIT 5
        """)
        analytics["top_problemes"] = [
            {"probleme": row[0], "count": row[1]}
            for row in cursor.fetchall()
        ]

        # Conversations par jour (7 derniers jours)
        cursor.execute("""
            SELECT DATE(created_at) as jour, COUNT(*) as total
            FROM conversations
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            GROUP BY jour
            ORDER BY jour ASC
        """)
        analytics["conversations_par_jour"] = [
            {"jour": str(row[0]), "count": row[1]}
            for row in cursor.fetchall()
        ]

        # Signalements en attente
        cursor.execute("""
            SELECT COUNT(*) FROM signalements
            WHERE statut = 'nouveau'
        """)
        analytics["signalements_nouveaux"] = cursor.fetchone()[0]

        return analytics

    except Exception as e:
        print("Erreur analytics :", e)
        return {}

    finally:
        cursor.close()
        conn.close()