import sqlite3
import os

# Funzione per connettersi al database
def connetti_db():
    return sqlite3.connect('spese_personali.db')

# MODULO 1: Gestione delle Categorie [cite: 56]
def gestione_categorie():
    print("\n--- GESTIONE CATEGORIE ---")
    nome = input("Inserisci il nome della categoria: ").strip()
    
    if not nome: # Verifica che il nome non sia vuoto [cite: 61]
        print("Errore: il nome non può essere vuoto.")
        return
    
    conn = connetti_db()
    cursor = conn.cursor()
    try:
        # Controllo esistenza e inserimento [cite: 62, 63]
        cursor.execute("INSERT INTO Categorie (nome) VALUES (?)", (nome,))
        conn.commit()
        print("Categoria inserita correttamente.") # [cite: 65]
    except sqlite3.IntegrityError:
        print("Errore: La categoria esiste già.") # [cite: 66]
    conn.close()

# MODULO 2: Inserimento di una Spesa [cite: 67]
def inserisci_spesa():
    print("\n--- INSERISCI SPESA ---")
    data = input("Data (YYYY-MM-DD): ") # [cite: 70]
    try:
        importo = float(input("Importo: ")) # [cite: 71]
        if importo <= 0: # Validazione importo [cite: 77]
            print("Errore: l'importo deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: Inserire un numero valido.")
        return

    cat_nome = input("Nome della categoria: ") # [cite: 72]
    conn = connetti_db()
    cursor = conn.cursor()
    
    # Verifica esistenza categoria [cite: 78]
    cursor.execute("SELECT id_categoria FROM Categorie WHERE nome = ?", (cat_nome,))
    res = cursor.fetchone()
    
    if not res:
        print("Errore: la categoria non esiste.") # [cite: 83]
    else:
        desc = input("Descrizione (facoltativa): ") # [cite: 73]
        cursor.execute("INSERT INTO Spese (data, importo, id_categoria, descrizione) VALUES (?, ?, ?, ?)",
                       (data, importo, res[0], desc)) # [cite: 79]
        conn.commit()
        print("Spesa inserita correttamente.") # [cite: 82]
    conn.close()

# MODULO 3: Definizione Budget Mensile [cite: 84]
def definisci_budget():
    print("\n--- DEFINISCI BUDGET MENSILE ---")
    mese = input("Mese (YYYY-MM): ") # [cite: 87]
    cat_nome = input("Nome della categoria: ") # [cite: 88]
    try:
        limite = float(input("Importo del budget: ")) # [cite: 89]
        if limite <= 0: # [cite: 91]
            print("Errore: il budget deve essere maggiore di zero.")
            return
    except ValueError:
        return

    conn = connetti_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id_categoria FROM Categorie WHERE nome = ?", (cat_nome,))
    res = cursor.fetchone() # [cite: 92]
    
    if res:
        # Inserimento o aggiornamento [cite: 93]
        cursor.execute("""INSERT INTO Budget (mese, id_categoria, importo_limite) 
                          VALUES (?, ?, ?) ON CONFLICT(mese, id_categoria) 
                          DO UPDATE SET importo_limite = excluded.importo_limite""", 
                       (mese, res[0], limite))
        conn.commit()
        print("Budget mensile salvato correttamente.") # [cite: 94]
    else:
        print("Errore: la categoria non esiste.")
    conn.close()

# MODULO 4: Visualizzazione Report [cite: 95]
def visualizza_report():
    while True:
        print("\n--- MENU REPORT ---") # [cite: 98]
        print("1. Totale spese per categoria") # [cite: 99]
        print("2. Spese mensili vs budget") # [cite: 100]
        print("3. Elenco completo delle spese") # [cite: 101]
        print("4. Ritorna al menu principale") # [cite: 102]
        
        scelta = input("Inserisci la tua scelta: ")
        conn = connetti_db()
        cursor = conn.cursor()

        if scelta == '1': # REPORT 1 [cite: 104]
            cursor.execute("""SELECT c.nome, SUM(s.importo) FROM Spese s 
                              JOIN Categorie c ON s.id_categoria = c.id_categoria GROUP BY c.nome""")
            print("\nCategoria | Totale Speso")
            for r in cursor.fetchall():
                print(f"{r[0]}.......{r[1]:.2f}") # [cite: 107]
        
        elif scelta == '2': # REPORT 2 [cite: 109]
            cursor.execute("""SELECT b.mese, c.nome, b.importo_limite, IFNULL(SUM(s.importo), 0)
                              FROM Budget b
                              JOIN Categorie c ON b.id_categoria = c.id_categoria
                              LEFT JOIN Spese s ON c.id_categoria = s.id_categoria 
                              AND strftime('%Y-%m', s.data) = b.mese
                              GROUP BY b.mese, c.nome""")
            for r in cursor.fetchall():
                stato = "SUPERAMENTO BUDGET" if r[3] > r[2] else "OK" # [cite: 112, 119]
                print(f"\nMese: {r[0]}\nCategoria: {r[1]}\nBudget: {r[2]}\nSpeso: {r[3]}\nStato: {stato}") # [cite: 115-119]
        
        elif scelta == '3': # REPORT 3 [cite: 120]
            cursor.execute("""SELECT s.data, c.nome, s.importo, s.descrizione 
                              FROM Spese s JOIN Categorie c ON s.id_categoria = c.id_categoria 
                              ORDER BY s.data""") # [cite: 101]
            print("\nData | Categoria | Importo | Descrizione")
            for r in cursor.fetchall():
                print(f"{r[0]} | {r[1]} | {r[2]:.2f} | {r[3]}") # [cite: 124]
        
        elif scelta == '4':
            break
        conn.close()

# Funzione Principale [cite: 30, 32]
def menu_principale():
    # Se il database non esiste, lo crea usando lo script SQL
    if not os.path.exists('spese_personali.db'):
        conn = connetti_db()
        # Assicurati che il file database.sql sia nella cartella 'sql' 
        with open('../sql/database.sql', 'r') as f:
            conn.executescript(f.read())
        conn.close()

    print("Benvenuto nel Sistema di Gestione Spese!") # [cite: 31]

    while True: # Ciclo iterativo 
        print("\n--- SISTEMA SPESE PERSONALI ---") # [cite: 41]
        print("1. Gestione Categorie") # [cite: 42]
        print("2. Inserisci Spesa") # [cite: 43]
        print("3. Definisci Budget Mensile") # [cite: 44]
        print("4. Visualizza Report") # [cite: 45]
        print("5. Esci") # [cite: 46]
        
        scelta = input("Inserisci la tua scelta: ") # [cite: 47, 50]
        
        if scelta == '1': gestione_categorie() # [cite: 52]
        elif scelta == '2': inserisci_spesa()
        elif scelta == '3': definisci_budget()
        elif scelta == '4': visualizza_report()
        elif scelta == '5': break # Uscita [cite: 46, 53]
        else: print("Scelta non valida. Riprovare.") # [cite: 54]

if __name__ == "__main__":
    menu_principale()