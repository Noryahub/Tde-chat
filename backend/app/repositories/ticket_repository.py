from backend.app.database.db import get_db_connection

def create_ticket(
    ticket_number,
    nom,
    email,
    telephone,
    localisation,
    description,
    intent
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO tickets (
        ticket_number,
        nom,
        email,
        telephone,
        localisation,
        description,
        intent
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            ticket_number,
            nom,
            email,
            telephone,
            localisation,
            description,
            intent
        )
    )

    conn.commit()

    ticket_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return ticket_id

def get_all_tickets():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM tickets
        ORDER BY created_at DESC
    """)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def get_ticket_by_id(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM tickets
        WHERE id = %s
    """, (ticket_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result

#RECUPERER LES TICKETS PAR UTILISATEURS
def get_ticket_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(""" SELECT * FROM tickets WHERE user_id = %s """, (user_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

#recuperer les tickets utilisateur resolus

def get_resolved_ticket_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(""" SELECT * FROM tickets WHERE user_id = %s AND statut = 'resolu' """, (user_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update_ticket_status(ticket_id, statut):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET statut = %s
        WHERE id = %s
    """, (statut, ticket_id))

    conn.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    conn.close()

    return affected_rows

def count_tickets():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM tickets
    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def delete_ticket(ticket_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tickets
        WHERE id = %s
    """, (ticket_id,))

    conn.commit()

    cursor.close()
    conn.close()

def count_open_tickets():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE statut = 'ouvert'
    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def count_in_progress_tickets():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE statut = 'en_cours'
    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def count_resolved_tickets():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE statut = 'resolu'
    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result