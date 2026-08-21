import logging

from backend.app.database.db import get_db_connection


def attach_anonymous_conversations(session_id, user_id):
    conn = get_db_connection()

    if not conn:
        raise RuntimeError("Erreur connexion base de données")

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE conversations
            SET user_id = %s
            WHERE session_id = %s
              AND user_id IS NULL
            """,
            (
                user_id,
                session_id
            )
        )
        attached = cursor.rowcount
        conn.commit()
        return attached

    except Exception as e:
        conn.rollback()
        logging.error(f"Erreur rattachement conversations anonymes : {e}")
        raise

    finally:
        cursor.close()
        conn.close()
