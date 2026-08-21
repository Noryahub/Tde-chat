from backend.app.database.db import get_db_connection

#initialisation de la conversation_id a null

#continute de la d'une mm conversation dont l'id est initialise


def get_user_history(user_id):

    conn = get_db_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    try:

        query = """
        SELECT
            c.id,
            c.session_id,
            c.predicted_intent,
            c.confidence_score,
            c.orientation_service,
            c.localisation,
            c.probleme,
            c.created_at
        FROM conversations c
        WHERE c.user_id = %s
        ORDER BY c.created_at DESC
        """

        cursor.execute(
            query,
            (user_id,)
        )

        conversations = cursor.fetchall()

        for conversation in conversations:

            cursor.execute(
                """
                SELECT
                    role,
                    content,
                    created_at
                FROM messages
                WHERE conversation_id = %s
                ORDER BY created_at ASC
                """,
                (conversation["id"],)
            )

            conversation["messages"] = (
                cursor.fetchall()
            )

        return conversations

    except Exception as e:

        print(
            "Erreur récupération historique utilisateur :",
            e
        )

        return []

    finally:

        cursor.close()
        conn.close()
def get_session_history(
    session_id,
    limit=10
):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        query = """
        SELECT
            m.role,
            m.content,
            m.created_at
        FROM messages m
        JOIN conversations c
            ON m.conversation_id = c.id
        WHERE c.session_id = %s
        ORDER BY m.created_at DESC
        LIMIT %s
        """

        cursor.execute(
            query,
            (session_id, limit)
        )

        rows = cursor.fetchall()

        return list(reversed(rows))

    except Exception as e:

        print(
            "Erreur récupération historique session :",
            e
        )

        return []

    finally:

        cursor.close()
        conn.close()

#modification de l'enregistrement des conversations
def save_conversation(
    user_id,
    conversation_id,
    session_id,
    user_message,
    intent,
    confidence,
    service,
    bot_response,
    localisation=None,
    probleme=None
):

    #if intent in ("followup", "fallback"):
       # return

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        # Recherche conversation existante
        if conversation_id is None:

            cursor.execute(
                """
                INSERT INTO conversations(
                    user_id,
                    session_id,
                    title,
                    predicted_intent,
                    confidence_score,
                    orientation_service,
                    localisation,
                    probleme
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    user_id,
                    session_id,
                    user_message[:60].strip(),  # premier message = titre
                    intent,
                    confidence,
                    service,
                    localisation,
                    probleme
                )
            )
            conversation_id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE conversations
                SET
                    predicted_intent=%s,
                    confidence_score=%s,
                    orientation_service=%s,
                    localisation=%s,
                    probleme=%s
                WHERE id=%s
                """,
                (
                    intent,
                    confidence,
                    service,
                    localisation,
                    probleme,
                    conversation_id
                )
            )

        # Message utilisateur
        cursor.execute(
            """
            INSERT INTO messages (
                conversation_id,
                role,
                content
            )
            VALUES (%s,%s,%s)
            """,
            (
                conversation_id,
                "user",
                user_message
            )
        )

        # Réponse assistant
        cursor.execute(
            """
            INSERT INTO messages (
                conversation_id,
                role,
                content
            )
            VALUES (%s,%s,%s)
            """,
            (
                conversation_id,
                "assistant",
                bot_response
            )
        )

        conn.commit()
        return conversation_id
    except Exception as e:

        print(
            "Erreur lors de l'enregistrement :",
            e
        )

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