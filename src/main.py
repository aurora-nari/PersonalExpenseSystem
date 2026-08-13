"""
Sistema di Gestione delle Spese Personali e del Budget
Autore: Aurora Nari
Matricola: 0082500046
Corso di laurea: L8 - Ingegneria Informatica e Intelligenza Artificiale
Esame: Fondamenti di Informatica
"""

import sqlite3
import os
import re
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR = os.path.join(PROJECT_DIR, "sql")
DB_FILE = os.path.join(SQL_DIR, "spese.db")


# ============================================================
# CONNESSIONE E CREAZIONE DEL DATABASE
# ============================================================

def get_connection():
    """Apre la connessione al database e attiva i vincoli di integrità referenziale."""
    os.makedirs(SQL_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_database():
    """Crea le tabelle eseguendo lo script sql/schema.sql."""
    conn = get_connection()
    schema_path = os.path.join(SQL_DIR, "schema.sql")

    try:
        with open(schema_path, "r", encoding="utf-8") as file:
            schema_sql = file.read()

        conn.executescript(schema_sql)
        conn.commit()

    except FileNotFoundError:
        print("Errore: il file sql/schema.sql non è stato trovato.")
        conn.close()
        raise SystemExit(1)

    except sqlite3.Error as errore:
        print(f"Errore nella creazione del database: {errore}")
        conn.close()
        raise SystemExit(1)

    conn.close()


# ============================================================
# FUNZIONI DI VALIDAZIONE
# ============================================================

def valida_data(testo):
    """Verifica che la stringa sia una data valida in formato YYYY-MM-DD."""
    try:
        datetime.strptime(testo, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def valida_mese(testo):
    """Verifica che la stringa sia un mese valido in formato YYYY-MM."""
    return bool(re.match(r"^[0-9]{4}-(0[1-9]|1[0-2])$", testo))


def leggi_float(prompt):
    """Legge un numero decimale da console, richiedendo un nuovo input in caso di errore di formato."""
    while True:
        valore = input(prompt).strip().replace(",", ".")
        try:
            return float(valore)
        except ValueError:
            print("Errore: inserire un numero valido (es. 25.50).")


# ============================================================
# MAIN
# ============================================================

def main():
    print("Benvenuto nel Sistema di Gestione delle Spese Personali e del Budget!")
    init_database()
    menu_principale()


# ============================================================
# MENU PRINCIPALE
# ============================================================

def menu_principale():
    while True:
        print("--------------------------")
        print("SISTEMA SPESE PERSONALI")
        print("--------------------------")
        print("1. Gestisci Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        print("--------------------------")
        scelta = input("Inserisci la tua scelta: ").strip()

        if scelta == "1":
            gestione_categorie()
        elif scelta == "2":
            inserimento_spesa()
        elif scelta == "3":
            definizione_budget_mensile()
        elif scelta == "4":
            visualizzazione_report()
        elif scelta == "5":
            print("Ricevuto il comando di uscita. Termino l'esecuzione del programma.\n")
            break
        else:
            print("Scelta non valida. Riprovare.\n")


# ============================================================
# MODULO 1 — GESTIONE DELLE CATEGORIE
# ============================================================

def esistenza_categoria(cursor, nome):
    cursor.execute("SELECT id FROM categorie WHERE nome = ?", (nome,))
    return cursor.fetchone()

def scegli_categoria():
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        nome_categoria = input("Nome della categoria: ").strip()
        categoria = esistenza_categoria(cursor, nome_categoria)

        if categoria:
            categoria_id = categoria[0]
            conn.close()
            return categoria_id

        print("Errore: la categoria non esiste.")

        while True:
            scelta = input(
                "1. Ritorna al menu principale per creare la categoria o verificarne il nome\n"
                "2. Prova ad inserire un altro nome\n"
                "Inserisci la tua scelta: "
            ).strip()

            if scelta == "1":
                print("Ritorno al menu principale ...\n")
                conn.close()
                return None

            if scelta == "2":
                break

            print("Scelta non valida. Inserire 1 oppure 2.\n")

def inserimento_categoria():
    nome = input("Nome della nuova categoria: ").strip()

    if nome == "":
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    if esistenza_categoria(cursor, nome):
        print("La categoria esiste già.")
    else:
        cursor.execute("INSERT INTO categorie (nome) VALUES (?)", (nome,))
        conn.commit()
        print("Categoria inserita correttamente.")

    conn.close()


def visualizza_categorie():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM categorie ORDER BY nome")
    righe = cursor.fetchall()
    conn.close()

    if not righe:
        print("Nessuna categoria presente.")
        return

    print("\nElenco categorie disponibili:")
    for id_cat, nome in righe:
        print(f"  {id_cat}. {nome}")


def gestione_categorie():
    while True:
        print("\n--------------------------")
        print("Gestione categorie")
        print("--------------------------")
        print("1. Visualizzazione delle categorie disponibili")
        print("2. Inserimento di una nuova categoria")
        print("3. Ritorno al menu principale")
        scelta = input("Inserisci la tua scelta: ").strip()

        if scelta == "1":
            visualizza_categorie()
        elif scelta == "2":
            inserimento_categoria()
        elif scelta == "3":
            print("3. Ritorno al menu principale ...\n")
            return
        else:
            print("Scelta non valida. Riprovare.")


# ============================================================
# MODULO 2 — INSERIMENTO DI UNA SPESA
# ============================================================

def inserimento_spesa():
    print("\n--------------------------")
    print("Inserimento spesa")
    print("--------------------------")

    categoria_id = scegli_categoria()
    if categoria_id is None:
        return

    while True:
        data = input("Data della spesa (formato YYYY-MM-DD): ").strip()
        if valida_data(data):
            break
        print("Errore: formato data non valido. Usare YYYY-MM-DD.\n")

    importo = leggi_float("Importo della spesa: ")
    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return

    descrizione = input(
        "Descrizione della spesa (facoltativa): "
    ).strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO spese "
        "(data, importo, categoria_id, descrizione) "
        "VALUES (?, ?, ?, ?)",
        (
            data,
            importo,
            categoria_id,
            descrizione if descrizione else None,
        ),
    )

    conn.commit()
    conn.close()
    print("Spesa inserita correttamente.\n")


# ============================================================
# MODULO 3 — DEFINIZIONE DEL BUDGET MENSILE
# ============================================================

def definizione_budget_mensile():
    print("\n--------------------------")
    print("Definizione budget mensile")
    print("--------------------------")

    categoria_id = scegli_categoria()
    if categoria_id is None:
        return

    while True:
        mese = input("Mese (YYYY-MM): ").strip()
        if valida_mese(mese):
            break
        print("Errore: formato mese non valido. Usare YYYY-MM.")

    importo = leggi_float("Importo del budget: ")
    if importo <= 0:
        print("Errore: il budget deve essere maggiore di zero.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Inserimento o aggiornamento (UPSERT) grazie al vincolo
    # UNIQUE(mese, categoria_id)
    cursor.execute("""
        INSERT INTO budget (mese, categoria_id, importo)
        VALUES (?, ?, ?)
        ON CONFLICT(mese, categoria_id)
        DO UPDATE SET importo = excluded.importo
    """, (mese, categoria_id, importo))

    conn.commit()
    conn.close()
    print("Budget mensile salvato correttamente.\n")


# ============================================================
# MODULO 4 — VISUALIZZAZIONE DEI REPORT
# ============================================================

def visualizzazione_report():
    while True:
        print("\n--------------------------")
        print("Visualizzazione report")
        print("--------------------------")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        scelta = input("Inserisci la tua scelta: ").strip()

        if scelta == "1":
            report_totale_per_categoria()
        elif scelta == "2":
            report_spese_vs_budget()
        elif scelta == "3":
            report_elenco_spese()
        elif scelta == "4":
            print("Ritorno al menu principale ...\n")
            return
        else:
            print("Scelta non valida. Riprovare.")


def report_totale_per_categoria():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.nome, SUM(s.importo) AS totale
        FROM categorie c
        JOIN spese s ON s.categoria_id = c.id
        GROUP BY c.nome
        ORDER BY c.nome
    """)
    righe = cursor.fetchall()
    conn.close()

    print(f"\n{'Categoria ':.<20}{' Totale Speso':.>20}")
    print("-" * 40)
    if not righe:
        print("Nessuna spesa registrata.")
        return
    for nome, totale in righe:
        importo_str = f"{totale:.2f}"
        print(f"{nome + ' ':.<20}{' ' + importo_str:.>20}")


def report_spese_vs_budget():
    while True:
        mese_filtro = input(
            "Selezionare il mese "
            "(YYYY-MM, lasciare vuoto per selezionare tutti i mesi): "
        ).strip()
        if mese_filtro == "" or valida_mese(mese_filtro):
            break
        print("Errore: formato mese non valido. Usare YYYY-MM.")

    categoria_filtro = input(
        "Selezionare la categoria "
        "(lasciare vuoto per selezionare tutte le categorie): "
    ).strip()

    conn = get_connection()
    cursor = conn.cursor()

    if categoria_filtro and not esistenza_categoria(cursor, categoria_filtro):
        print("Errore: la categoria non esiste.")
        conn.close()
        return

    cursor.execute("""
        SELECT b.mese, c.nome, b.importo AS budget,
               COALESCE((
                   SELECT SUM(s.importo)
                   FROM spese s
                   WHERE s.categoria_id = b.categoria_id
                     AND strftime('%Y-%m', s.data) = b.mese
               ), 0) AS speso
        FROM budget b
        JOIN categorie c ON c.id = b.categoria_id
        WHERE (? = '' OR b.mese = ?)
          AND (? = '' OR c.nome = ? COLLATE NOCASE)
        ORDER BY b.mese, c.nome
    """, (
        mese_filtro,
        mese_filtro,
        categoria_filtro,
        categoria_filtro
    ))

    righe = cursor.fetchall()
    conn.close()

    if not righe:
        print("Nessun budget definito per i filtri indicati.")
        return

    for mese, nome, budget_val, speso in righe:
        stato = (
            "SUPERAMENTO BUDGET."
            if speso > budget_val
            else "BUDGET RISPETTATO."
        )

        print(f"\nMese: {mese}")
        print(f"\nCategoria: {nome}")
        print(f"Budget: {budget_val:.2f}")
        print(f"Speso: {speso:.2f}")
        print(f"Stato: {stato}")


def report_elenco_spese():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.data, c.nome, s.importo, COALESCE(s.descrizione, '')
        FROM spese s
        JOIN categorie c ON c.id = s.categoria_id
        ORDER BY s.data
    """)
    righe = cursor.fetchall()
    conn.close()

    def colonna(testo, larghezza, ultima=False):
        if ultima:
            return f"{testo + ' ':.<{larghezza}}"
        return f"{testo + ' ':.<{larghezza - 1}} "

    intestazione = (
        colonna("Data", 16)
        + colonna("Categoria", 26)
        + colonna("Importo", 12)
        + colonna("Descrizione", 37, ultima=True)
    )
    print(f"\n{intestazione}")
    print("-" * len(intestazione))

    if not righe:
        print("Nessuna spesa registrata.")
        return

    for data, nome, importo, descrizione in righe:
        importo_str = f"{importo:.2f}"
        riga = (
            colonna(data, 16)
            + colonna(nome, 26)
            + colonna(importo_str, 12)
            + colonna(descrizione, 37, ultima=True)
        )
        print(riga)


if __name__ == "__main__":
    main()