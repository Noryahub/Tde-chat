import logging

from backend.app.database.db import get_db_connection


def create_oauth_state(
    state_hash,
    session_id,
    redirect_path,
    ttl_seconds
):
    conn = get_db_connection()

    if not conn:
        raise RuntimeError("Erreur connexion base de données")

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
        INSERT INTO oauth_login_states (
            state_hash,
            session_id,
            redirect_path,
            expires_at
        )
        VALUES (%s, %s, %s, UTC_TIMESTAMP() + INTERVAL %s SECOND)
        """,
        (
            state_hash,
            session_id,
            redirect_path,
            ttl_seconds
        )
    )
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Erreur création state OAuth : {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def consume_oauth_state(state_hash):
    conn = get_db_connection()

    if not conn:
        raise RuntimeError("Erreur connexion base de données")

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            UPDATE oauth_login_states
            SET used_at = UTC_TIMESTAMP()
            WHERE state_hash = %s
              AND used_at IS NULL
              AND expires_at > UTC_TIMESTAMP()
            """,
            (state_hash,)
        )

        if cursor.rowcount != 1:
            conn.rollback()
            return None

        cursor.execute(
            """
            SELECT
                state_hash,
                session_id,
                redirect_path,
                expires_at,
                used_at
            FROM oauth_login_states
            WHERE state_hash = %s
            """,
            (state_hash,)
        )

        row = cursor.fetchone()
        conn.commit()
        return row

    except Exception as e:
        conn.rollback()
        logging.error(f"Erreur consommation state OAuth : {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def create_exchange_code(
    code_hash,
    user_id,
    attached_conversations,
    ttl_seconds
):
    conn = get_db_connection()

    if not conn:
        raise RuntimeError("Erreur connexion base de données")

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
        INSERT INTO oauth_exchange_codes (
            code_hash,
            user_id,
            attached_conversations,
            expires_at
        )
        VALUES (%s, %s, %s, UTC_TIMESTAMP() + INTERVAL %s SECOND)
        """,
        (
            code_hash,
            user_id,
            attached_conversations,
            ttl_seconds
        )
    )
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Erreur création code échange OAuth : {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def consume_exchange_code(code_hash):
    conn = get_db_connection()

    if not conn:
        raise RuntimeError("Erreur connexion base de données")

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            UPDATE oauth_exchange_codes
            SET used_at = UTC_TIMESTAMP()
            WHERE code_hash = %s
              AND used_at IS NULL
              AND expires_at > UTC_TIMESTAMP()
            """,
            (code_hash,)
        )

        if cursor.rowcount != 1:
            conn.rollback()
            return None

        cursor.execute(
            """
            SELECT
                code_hash,
                user_id,
                attached_conversations,
                expires_at,
                used_at
            FROM oauth_exchange_codes
            WHERE code_hash = %s
            """,
            (code_hash,)
        )

        row = cursor.fetchone()
        conn.commit()
        return row

    except Exception as e:
        conn.rollback()
        logging.error(f"Erreur consommation code échange OAuth : {e}")
        raise
    finally:
        cursor.close()
        conn.close()
