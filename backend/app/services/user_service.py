import re
import time
import logging

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from backend.app.database.db import get_db_connection


# =========================================
# RATE LIMITING
# =========================================

login_attempts = {}


def is_rate_limited(email):

    attempts, last_time = login_attempts.get(
        email,
        (0, 0)
    )

    # reset après 60 secondes
    if time.time() - last_time > 60:

        login_attempts[email] = (
            0,
            time.time()
        )

        return False

    return attempts >= 5


# =========================================
# VALIDATION
# =========================================

def validate_user(email, password):

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not email or not re.match(email_regex, email):
        return False, "Email invalide"

    if not password or len(password) < 6:
        return False, "Mot de passe trop court"

    return True, None


# =========================================
# GET USER
# =========================================

def get_user_by_email(email):

    conn = get_db_connection()

    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:

        query = """
        SELECT
            id,
            nom,
            email,
            role,
            created_at
        FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))

        return cursor.fetchone()

    except Exception as e:

        logging.error(
            f"Erreur récupération utilisateur : {e}"
        )

        return None

    finally:

        cursor.close()
        conn.close()


# =========================================
# CREATE USER
# =========================================

def create_user(
    email,
    password,
    nom=None,
    role="user"
):

    conn = get_db_connection()

    if not conn:
        return None, "Erreur connexion base de données"

    cursor = conn.cursor()

    try:

        # validation
        valid, error = validate_user(
            email,
            password
        )

        if not valid:
            return None, error

        # vérifier si existe déjà
        query = """
        SELECT id
        FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))

        if cursor.fetchone():
            return None, "Utilisateur déjà existant"

        # hash mot de passe
        hashed_password = generate_password_hash(
            password
        )

        # insertion
        query = """
        INSERT INTO users (
            nom,
            email,
            password,
            role
        )
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                nom,
                email,
                hashed_password,
                role
            )
        )

        conn.commit()

        return cursor.lastrowid, None

    except Exception as e:

        logging.error(
            f"Erreur création utilisateur : {e}"
        )

        return None, "Erreur serveur"

    finally:

        cursor.close()
        conn.close()


# =========================================
# AUTHENTIFICATION
# =========================================

def authenticate_user(email, password):

    if is_rate_limited(email):

        logging.warning(
            f"Trop de tentatives : {email}"
        )

        return None

    conn = get_db_connection()

    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:

        query = """
        SELECT
            id,
            password,
            role
        FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        if user and check_password_hash(
            user["password"],
            password
        ):

            # reset compteur
            login_attempts[email] = (
                0,
                time.time()
            )

            # mise à jour last_login
            update_query = """
            UPDATE users
            SET last_login = CURRENT_TIMESTAMP
            WHERE id = %s
            """

            cursor.execute(
                update_query,
                (user["id"],)
            )

            conn.commit()

            return {
                "id": user["id"],
                "role": user["role"]
            }

        # échec connexion
        attempts, _ = login_attempts.get(
            email,
            (0, time.time())
        )

        login_attempts[email] = (
            attempts + 1,
            time.time()
        )

        return None

    except Exception as e:

        logging.error(
            f"Erreur authentification : {e}"
        )

        return None

    finally:

        cursor.close()
        conn.close()