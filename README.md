# PersonalExpenseSystem

Sistema a console per la gestione delle spese personali e del budget mensile.

Il programma è progettato per singolo utente e consente di:

- gestire le categorie di spesa;
- inserire spese con data, importo, categoria e descrizione opzionale;
- definire o aggiornare un limite mensile di spesa per categoria;
- visualizzare report riepilogativi sul comportamento di spesa.

I report riepilogativi permettono di:

- visualizzare il totale delle spese per categoria;
- confrontare le spese mensili con il budget, indicando il rispetto o il superamento del budget;
- visualizzare l'elenco completo delle spese ordinato per data.

## Requisiti

- Python 3.8 o versione successiva;
- SQLite 3, utilizzato tramite il modulo standard `sqlite3` di Python;
- nessuna libreria Python esterna;
- librerie standard utilizzate: os, re, datetime.

Poiché il modulo `sqlite3` fa parte della libreria standard di Python, non è necessario installare separatamente un server SQLite.

## Repository GitHub

Il link al repository GitHub è https://github.com/aurora-nari/PersonalExpenseSystem

## Struttura del repository

```text
PersonalExpenseSystem/
├── src/
│   └── main.py
├── sql/
│   ├── schema.sql
│   └── database.sql
└── demo/
│   └── video dimostrativo
└── README.md
```

### `src/main.py`

Contiene il codice sorgente dell'applicazione, il menu a console, la validazione degli input, le operazioni sul database e i report SQL.

### `sql/schema.sql`

Contiene esclusivamente lo schema del database e viene eseguito automaticamente dal programma all'avvio.

Contiene:

- `PRAGMA foreign_keys = ON`;
- `CREATE TABLE` per `categorie`;
- `CREATE TABLE` per `spese`;
- `CREATE TABLE` per `budget`;
- i vincoli di integrità richiesti.

### `sql/database.sql`

Contiene lo script SQL completo utilizzato nella documentazione. Comprende:

- creazione delle tabelle;
- vincoli di integrità;
- dati di esempio tramite `INSERT`;
- query dimostrative dei report.

Il programma non esegue automaticamente questo file, perché contiene gli inserimenti dei dati di esempio.
Per la creazione del database, viene, invece, eseguito `schema.sql`.

### `demo/`

Contiene il video dimostrativo sull'utilizzo del programma. Il video mostra:

1. l'avvio del programma;
2. l'utilizzo dei menu;
3. l'inserimento di dati;
4. la generazione di un report.

## Compilazione

Non è richiesta compilazione, poiché Python è un linguaggio interpretato.

## Avvio del programma

Aprire un terminale nella cartella principale `PersonalExpenseSystem` ed eseguire:

```bash
python src/main.py
```

Su alcuni sistemi Windows potrebbe essere necessario usare:

```powershell
py src/main.py
```

Il programma individua automaticamente la cartella `sql`, legge il file `sql/schema.sql` e crea il database SQLite `sql/spese.db` al primo avvio.

## Funzionamento del database

Il database viene creato automaticamente con tre tabelle:

### `categorie`

- `id`: chiave primaria;
- `nome`: obbligatorio, univoco e confrontato senza distinzione tra maiuscole e minuscole.

### `spese`

- `id`: chiave primaria;
- `data`: data nel formato `YYYY-MM-DD`;
- `importo`: deve essere maggiore di zero;
- `categoria_id`: chiave esterna verso `categorie(id)`;
- `descrizione`: facoltativa.

### `budget`

- `id`: chiave primaria;
- `mese`: mese nel formato `YYYY-MM`;
- `categoria_id`: chiave esterna verso `categorie(id)`;
- `importo`: deve essere maggiore di zero;
- `UNIQUE (mese, categoria_id)`: impedisce più budget per la stessa categoria nello stesso mese.

## Dati di esempio

I dati di esempio sono presenti esclusivamente in `sql/database.sql` e sono coerenti con lo schema del database:

- categorie: `Alimentari`, `Trasporti`, `Svago`;
- spese e budget per il mese `2026-01`;
- budget mensili rispettivamente di `600.00`, `200.00` e `100.00`.

## Ripristino del database

Per ricreare il database da zero (database vuoto):

1. chiudere il programma;
2. eliminare il file `sql/spese.db`, se presente;
3. eseguire nuovamente:

```bash
python src/main.py
```

Il programma ricreerà automaticamente le tabelle a partire da `sql/schema.sql`.

## Esecuzione

Una volta dato il comando da terminale:

```bash
python src/main.py
```
Il sistema apre il menu principale per la scelta della funzione da parte dell'utente.
Inserire un valore da 1 a 5, a seconda dell'operazione da eseguire.
Valori superiori a 5 restituiscono un messaggio di errore.

### Gestione delle categorie

Scegliendo 1 nel menu principale, l'utente accede al menu di gestione delle categorie.

- Scegliendo 1 in Gestione delle Categorie, il sistema restituisce l'elenco delle categorie o un avviso nel caso non esistano categorie.

- Scegliendo 2 in Gestione delle Categorie, l'utente dovrà inserire il nome della categoria da creare.

	Ai fini dell'inserimento della categoria, la funzione di inserimento non è case sensitive: Alimentari oppure alimentari sono la stessa categoria.

- Scegliendo 3 in Gestione delle Categorie si ritorna al menu principale.

### Inserimento di una spesa

Scegliendo 2 nel menu principale, l'utente accede alla funzione di inserimento di una spesa.
L'utente dovrà inserire la categoria.

Nel caso di categoria non esistente (la categoria non esiste oppure il nome è stato inserito in maniera errata), la funzione restituirà un menu di scelta.
- Scegliendo 1, l'utente torna al menu principale per poter creare la nuova categoria o verificare i nomi delle categorie esistenti tramite Gestione delle Categorie.
- Scegliendo 2, l'utente può provare ad inserire un nuovo nome.

Nel caso il nome della categoria esista, all'utente viene chiesto di inserire la data nel formato YYYY-MM-DD.

In caso di errore nel formato della data, il sistema restituisce un messaggio di errore e resta in attesa di una data valida.

Inserita una data valida, l'utente deve inserire l'importo della spesa.

Inserito l'importo, il sistema chiede all'utente una descrizione facoltativa delle spesa.

Completati gli inserimenti, il sistema restituisce un messaggio di avviso sull'esito positivo dell'operazione e ritorna al menu principale.

### Gestione del budget mensile

Scegliendo 3 nel menu principale, l'utente accede alla funzione di definizione del budget mensile di spesa.

L'utente dovrà inserire la categoria.

Nel caso di categoria non esistente (la categoria non esiste oppure il nome è stato inserito in maniera errata), la funzione restituirà un menu di scelta.
- Scegliendo 1, l'utente torna al menu principale per poter creare la nuova categoria o verificare i nomi delle categorie esistenti tramite Gestione delle Categorie.
- Scegliendo 2, l'utente può provare ad inserire un nuovo nome.

Nel caso il nome della categoria esista, all'utente viene chiesto di inserire il mese per cui vuole definire il budget nel formato YYYY-MM.

In caso di errore nel formato del mese, il sistema restituisce un messaggio di errore e resta in attesa di un mese valido.

Inserito un mese valido, l'utente deve inserire il valore del budget.

Completati gli inserimenti, il sistema restituisce un messaggio di avviso sull'esito positivo dell'operazione e ritorna al menu principale.

### Visualizzazione dei report
Scegliendo 4 nel menu principale, l'utente accede alla funzione di visualizzazione dei report.

Inserire un valore da 1 a 4, a seconda dell'operazione da fare.

Valori superiori a 4 restituiranno un messaggio di errore.

Inserendo 4, il sistema ritorna al menu principale.

Inserendo 1 o 3, il sistema mostra direttamente l'output del report corrispondente.

Inserendo 2, all'utente viene richiesto di inserire un mese (nessuna selezione per scegliere tutti i mesi) e una categoria (nessuna selezione per tutte le categorie).

Quindi, il sistema emetterà il report sulla base dei filtri impostati.
- In caso di formato mese non valido, il sistema emette un avvertimento e resta in attesa di un formato mese valido (oppure si preme invio per scegliere tutti i mesi).
- In caso di categoria non esistente, il sistema restituisce un errore e ritorna al menu di Visualizzazione dei report.
