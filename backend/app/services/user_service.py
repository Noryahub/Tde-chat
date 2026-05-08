import re
import time
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from backend.app.database.db import get_db_connection
# Rate limiting (mémoire simple)
login_attempts = {}

def is_rate_limited(email):
    attempts, last_time = login_attempts.get(email, (0, 0))

    # reset après 60 secondes
    if time.time() - last_time > 60:
        login_attempts[email] = (0, time.time())
        return False

    return attempts >= 5

# Validation utilisateur
def validate_user(email, password):

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not email or not re.match(email_regex, email):
        return False, "Email invalide"

    if not password or len(password) < 6:
        return False, "Mot de passe trop court"

    return True, None

# Récupérer utilisateur
def get_user_by_email(email):
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor()

    try:
        query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result[0] if result else None

    except Exception as e:
        logging.error(f"Erreur récupération utilisateur: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

# Création utilisateur
def create_user(email, password):

    conn = get_db_connection()
    if not conn:
        return None, "Erreur connexion base de données"

    cursor = conn.cursor()

    try:
        # validation
        valid, error = validate_user(email, password)
        if not valid:
            return None, error

        # vérifier si existe déjà (optimisé, sans double connexion)
        query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        if cursor.fetchone():
            return None, "Utilisateur déjà existant"

        # hash du mot de passe
        hashed_password = generate_password_hash(password)

        # insertion
        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        cursor.execute(query, (email, hashed_password))
        conn.commit()

        return cursor.lastrowid, None

    except Exception as e:
        logging.error(f"Erreur création utilisateur: {e}")
        return None, "Erreur serveur"

    finally:
        cursor.close()
        conn.close()

# Authentification
def authenticate_user(email, password):

    if is_rate_limited(email):
        return None

    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor()

    try:
        query = "SELECT id, password FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result and check_password_hash(result[1], password):
            # reset compteur
            login_attempts[email] = (0, time.time())
            return result[0]

        # échec
        attempts, _ = login_attempts.get(email, (0, time.time()))
        login_attempts[email] = (attempts + 1, time.time())

        return None

    except Exception as e:
        logging.error(f"Erreur authentification: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

