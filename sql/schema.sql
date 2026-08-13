-- ============================================================
-- Sistema di Gestione delle Spese Personali e del Budget
-- Autore: Aurora Nari
-- Matricola: 0082500046
-- Corso di laurea: L8 - Ingegneria Informatica e Intelligenza Artificiale
-- Esame: Fondamenti di Informatica
-- ============================================================
-- Script SQL per la creazione dello schema del database
-- Questo file contiene solo la struttura del database
-- I dati di esempio sono riportati nel file database.sql
-- Motore utilizzato: SQLite 3
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Tabella: categorie
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categorie (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome    TEXT NOT NULL UNIQUE COLLATE NOCASE
);

-- ------------------------------------------------------------
-- Tabella: spese
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS spese (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    data          TEXT NOT NULL,
    importo       REAL NOT NULL CHECK (importo > 0),
    categoria_id  INTEGER NOT NULL,
    descrizione   TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

-- ------------------------------------------------------------
-- Tabella: budget
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS budget (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    mese          TEXT NOT NULL,
    categoria_id  INTEGER NOT NULL,
    importo       REAL NOT NULL CHECK (importo > 0),
    FOREIGN KEY (categoria_id) REFERENCES categorie(id),
    UNIQUE (mese, categoria_id)
);
