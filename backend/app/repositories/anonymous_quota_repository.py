from backend.app.database.db import get_db_connection


DEFAULT_ANONYMOUS_MESSAGES_LIMIT = 5


class AnonymousQuotaRepository:
    @staticmethod
    def ensure_session(
        session_id: str,
        messages_limit: int = DEFAULT_ANONYMOUS_MESSAGES_LIMIT
    ) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO anonymous_sessions (
                    session_id,
                    messages_used,
                    messages_limit
                )
                VALUES (%s, 0, %s)
                ON DUPLICATE KEY UPDATE
                    session_id = session_id
                """,
                (
                    session_id,
                    messages_limit
                )
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def consume_message(session_id: str) -> bool:
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE anonymous_sessions
                SET
                    messages_used = messages_used + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE session_id = %s
                  AND messages_used < messages_limit
                """,
                (session_id,)
            )
            conn.commit()
            return cursor.rowcount == 1
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_quota(session_id: str) -> dict | None:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    messages_used,
                    messages_limit,
                    GREATEST(messages_limit - messages_used, 0)
                        AS messages_remaining
                FROM anonymous_sessions
                WHERE session_id = %s
                """,
                (session_id,)
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
