-- ============================================================
-- Sistema di Gestione delle Spese Personali e del Budget
-- Autore: Aurora Nari
-- Matricola: 0082500046
-- Corso di laurea: L8 - Ingegneria Informatica e Intelligenza Artificiale
-- Esame: Fondamenti di Informatica
-- ============================================================
-- Script SQL completo
-- Consente la creazione del database
-- Consente l'inserimento di dati di esempio
-- Motore utilizzato: SQLite 3
-- ============================================================

-- ============================================================
-- Script di creazione del database
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

-- ============================================================
-- Dati di esempio
-- ============================================================

-- CATEGORIE
INSERT INTO categorie (nome) VALUES ('Alimentari');
INSERT INTO categorie (nome) VALUES ('Trasporti');
INSERT INTO categorie (nome) VALUES ('Svago');

-- SPESE
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES
    ('2026-01-03', 123.50, 1, 'Spesa settimanale'),
    ('2026-01-08', 63.90, 1, 'Cena'),
    ('2026-01-09', 89.30, 1, 'Spesa settimanale'),
    ('2026-01-15', 25.00, 1, 'Pranzo'),
    ('2026-01-16', 83.50, 1, 'Spesa settimanale'),
    ('2026-01-23', 114.80, 1, 'Spesa settimanale'),
    ('2026-01-30', 102.45, 1, 'Spesa settimanale'),
    ('2026-01-10', 85.00, 2, 'Rifornimento benzina'),
    ('2026-01-31', 75.00, 2, 'Abbonamento mensile bus'),
    ('2026-01-21', 68.00, 3, 'Biglietti concerto'),
    ('2026-01-25', 12.00, 3, 'Cinema');

-- BUDGET MENSILE
INSERT INTO budget (mese, categoria_id, importo) VALUES
    ('2026-01', 1, 600.00),
    ('2026-01', 2, 200.00),
    ('2026-01', 3, 100.00);

-- ============================================================
-- Query di esempio usate dai report
-- ============================================================

-- REPORT 1: Totale spese per categoria
SELECT c.nome, SUM(s.importo) AS totale
FROM categorie c
JOIN spese s ON s.categoria_id = c.id
GROUP BY c.nome
ORDER BY c.nome;

-- REPORT 2: Spese mensili vs budget
SELECT b.mese, c.nome, b.importo AS budget,
       COALESCE(SUM(s.importo), 0) AS speso
FROM budget b
JOIN categorie c ON c.id = b.categoria_id
LEFT JOIN spese s ON s.categoria_id = b.categoria_id
                  AND strftime('%Y-%m', s.data) = b.mese
GROUP BY b.mese, c.nome
ORDER BY b.mese, c.nome;

-- REPORT 3: Elenco completo delle spese ordinato per data
SELECT s.data, c.nome, s.importo, s.descrizione
FROM spese s
JOIN categorie c ON c.id = s.categoria_id
ORDER BY s.data;
