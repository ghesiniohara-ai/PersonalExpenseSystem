-- Creazione delle tabelle con vincoli di integrità
CREATE TABLE Categorie (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL
);

CREATE TABLE Spese (
    id_spesa INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL, -- Formato YYYY-MM-DD
    importo REAL NOT NULL CHECK(importo > 0),
    id_categoria INTEGER NOT NULL,
    descrizione TEXT,
    FOREIGN KEY (id_categoria) REFERENCES Categorie(id_categoria)
);

CREATE TABLE Budget (
    id_budget INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT NOT NULL, -- Formato YYYY-MM
    id_categoria INTEGER NOT NULL,
    importo_limite REAL NOT NULL CHECK(importo_limite > 0),
    FOREIGN KEY (id_categoria) REFERENCES Categorie(id_categoria),
    UNIQUE(mese, id_categoria)
);

-- Inserimento dati di esempio per la demo
INSERT INTO Categorie (nome) VALUES ('Alimentari'), ('Trasporti'), ('Svago');
INSERT INTO Spese (data, importo, id_categoria, descrizione) VALUES ('2026-01-15', 25.50, 1, 'Spesa pranzo');
INSERT INTO Budget (mese, id_categoria, importo_limite) VALUES ('2026-01', 1, 300.00);
