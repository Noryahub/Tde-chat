import sys
import os

# ajouter le dossier racine au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.database.db import get_db_connection

conn = get_db_connection()

if conn:
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")

    for table in cursor.fetchall():
        print(table)

    conn.close()