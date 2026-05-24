import sqlite3
import pandas as pd

DB_PATH = "pulsejob.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS offres (
            id TEXT PRIMARY KEY,
            titre TEXT,
            entreprise TEXT,
            localisation TEXT,
            departement TEXT,
            type_contrat TEXT,
            date_publication TEXT,
            description TEXT,
            competences TEXT,
            salaire TEXT,
            experience TEXT,
            lien TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès")

def inserer_offre(offre):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO offres VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, offre)
        conn.commit()
    except Exception as e:
        print(f"Erreur insertion : {e}")
    finally:
        conn.close()

def get_toutes_offres():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM offres", conn)
    conn.close()
    return df