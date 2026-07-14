from backend.app.database.db import get_db_connection

class HistoryRepository:
    @staticmethod
    def get_messages_by_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT
            c.user_id,
            c.id AS conversation_id,
            m.id AS message_id,
            m.content,
            m.role,
            m.created_at
        FROM conversations c
        INNER JOIN messages m
            ON m.conversation_id = c.id
        WHERE c.user_id = %s
        ORDER BY m.created_at ASC;
                """, (user_id,))
        results =  cursor.fetchall()
        cursor.close()
        conn.close()
        return results
