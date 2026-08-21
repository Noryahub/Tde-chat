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
            auth_provider,
            provider_subject,
            email_verified,
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


def get_user_by_provider_subject(auth_provider, provider_subject):

    conn = get_db_connection()

    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                id,
                nom,
                email,
                role,
                auth_provider,
                provider_subject,
                email_verified,
                is_active
            FROM users
            WHERE auth_provider = %s
              AND provider_subject = %s
            """,
            (
                auth_provider,
                provider_subject
            )
        )

        return cursor.fetchone()

    except Exception as e:
        logging.error(f"Erreur récupération utilisateur OAuth : {e}")
        return None

    finally:
        cursor.close()
        conn.close()


def get_or_create_google_user(
    email,
    nom,
    provider_subject,
    email_verified
):

    existing = get_user_by_provider_subject(
        "google",
        provider_subject
    )

    if existing:
        update_last_login(existing["id"])
        return existing, None

    existing_by_email = get_user_by_email(email)

    if existing_by_email:
        linked_user, error = link_google_to_existing_user(
            user_id=existing_by_email["id"],
            provider_subject=provider_subject,
            email_verified=email_verified
        )

        if error:
            return None, error

        return linked_user, None

    return create_google_user(
        email=email,
        nom=nom,
        provider_subject=provider_subject,
        email_verified=email_verified
    )


def create_google_user(
    email,
    nom,
    provider_subject,
    email_verified
):

    conn = get_db_connection()

    if not conn:
        return None, "Erreur connexion base de données"

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (
                nom,
                email,
                password,
                role,
                auth_provider,
                provider_subject,
                email_verified,
                last_login
            )
            VALUES (%s, %s, NULL, 'user', 'google', %s, %s, CURRENT_TIMESTAMP)
            """,
            (
                nom,
                email,
                provider_subject,
                email_verified
            )
        )

        user_id = cursor.lastrowid
        conn.commit()

        return get_user_by_id(user_id), None

    except Exception as e:
        conn.rollback()
        logging.error(f"Erreur création utilisateur Google : {e}")
        return None, "Erreur serveur"

    finally:
        cursor.close()
        conn.close()


def link_google_to_existing_user(
    user_id,
    provider_subject,
    email_verified
):

    conn = get_db_connection()

    if not conn:
        return None, "Erreur connexion base de données"

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET auth_provider = 'google',
                provider_subject = %s,
                email_verified = %s,
                last_login = CURRENT_TIMESTAMP
            WHERE id = %s
              AND (
                    provider_subject IS NULL
                    OR provider_subject = %s
                  )
            """,
            (
                provider_subject,
                email_verified,
                user_id,
                provider_subject
            )
        )

        if cursor.rowcount != 1:
            conn.rollback()
            return None, "Compte déjà associé à un autre fournisseur"

        conn.commit()
        return get_user_by_id(user_id), None

    except Exception as e:
        conn.rollback()
        logging.error(f"Erreur liaison utilisateur Google : {e}")
        return None, "Erreur serveur"

    finally:
        cursor.close()
        conn.close()


def update_last_login(user_id):

    conn = get_db_connection()

    if not conn:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET last_login = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (user_id,)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Erreur mise à jour last_login : {e}")
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


#
def get_user_by_id(user_id):

    conn = get_db_connection()

    if not conn:
        return None

    cursor = conn.cursor(
        dictionary=True
    )

    try:

        query = """
        SELECT
            id,
            nom,
            email,
            role,
            auth_provider,
            provider_subject,
            email_verified,
            is_active,
            last_login,
            created_at,
            updated_at
        FROM users
        WHERE id = %s
        """

        cursor.execute(
            query,
            (user_id,)
        )

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

    cursor = conn.cursor(
        dictionary=True
    )

    try:

        query = """
        SELECT
            id,
            nom,
            email,
            password,
            role,
            is_active
        FROM users
        WHERE email = %s
        """

        cursor.execute(
            query,
            (email,)
        )

        user = cursor.fetchone()

        if not user:
            return None

        # compte désactivé
        if not user["is_active"]:

            logging.warning(
                f"Compte désactivé : {email}"
            )

            return None

        if user["password"] and check_password_hash(
            user["password"],
            password
        ):

            # reset compteur
            login_attempts[email] = (
                0,
                time.time()
            )

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
                "nom": user["nom"],
                "email": user["email"],
                "role": user["role"]
            }

        # mot de passe incorrect
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
