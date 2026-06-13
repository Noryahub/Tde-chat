from backend.app.database.db import get_db_connection


class AnalyticsRepository:

    @staticmethod
    def get_total_conversations():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM conversations
        """)

        result = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def get_signalements_nouveaux():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM signalements
            WHERE statut = 'nouveau'
        """)

        result = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def get_top_intents(limit=5):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                predicted_intent AS intent,
                COUNT(*) AS count
            FROM conversations
            WHERE predicted_intent IS NOT NULL
            GROUP BY predicted_intent
            ORDER BY count DESC
            LIMIT %s
        """, (limit,))

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    @staticmethod
    def get_top_localisations(limit=5):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                localisation,
                COUNT(*) AS count
            FROM conversations
            WHERE localisation IS NOT NULL
            GROUP BY localisation
            ORDER BY count DESC
            LIMIT %s
        """, (limit,))

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    @staticmethod
    def get_top_problemes(limit=5):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                probleme,
                COUNT(*) AS count
            FROM conversations
            WHERE probleme IS NOT NULL
            GROUP BY probleme
            ORDER BY count DESC
            LIMIT %s
        """, (limit,))

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    @staticmethod
    def get_conversations_par_jour():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                DATE(created_at) AS jour,
                COUNT(*) AS count
            FROM conversations
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            GROUP BY DATE(created_at)
            ORDER BY jour
        """)

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    @staticmethod
    def get_latest_signalements(limit=8):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                localisation,
                probleme,
                statut,
                created_at
            FROM signalements
            ORDER BY created_at DESC
            LIMIT %s
        """, (limit,))

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results