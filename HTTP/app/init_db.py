import sqlite3

# Connessione al database
conn = sqlite3.connect("./HTTP/app/database.db")
cur = conn.cursor()

# Creazione della tabella utenti
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Inserimento di dati di test (controlla se l'utente esiste già)
users = [
    ("admin", "supersecret"),
    ("user1", "password123"),
    ("guest", "guest123")
]

# Controllo se l'utente esiste già
for username, password in users:
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

# Test della query (restituisce l'utente user1)
cur.execute("""
SELECT * FROM users where id = 2
""")
result = cur.fetchone()
print(result)

# Test della query (restituisce None)
cur.execute("""
SELECT * FROM users where id = 4
""")
result = cur.fetchone()
print(result)


# Salvataggio e chiusura connessione
conn.commit()
conn.close()
print("Database creato con successo!")
