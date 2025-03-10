import sqlite3
from datetime import datetime

# Connessione al database
conn = sqlite3.connect("./HTTP/app/database.db")
cur = conn.cursor()

# Creazione della tabella utenti
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT UNIQUE,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Creazione della tabella transazioni (simuliamo un'app bancaria)
cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    type TEXT CHECK(type IN ('deposit', 'withdrawal')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# Inserimento di utenti finti
users = [
    ("admin", "supersecret", "admin@example.com", "admin"),
    ("user1", "password123", "user1@example.com", "user"),
    ("guest", "guest123", "guest@example.com", "guest"),
    ("john_doe", "qwerty", "john@example.com", "user"),
    ("alice_smith", "letmein", "alice@example.com", "user")
]

for username, password, email, role in users:
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)", 
                    (username, password, email, role))

# Inserimento di transazioni casuali
transactions = [
    (1, 500.00, 'deposit'),
    (2, -200.00, 'withdrawal'),
    (3, 1500.00, 'deposit'),
    (1, -50.00, 'withdrawal')
]

for user_id, amount, t_type in transactions:
    cur.execute("INSERT INTO transactions (user_id, amount, type) VALUES (?, ?, ?)", 
                (user_id, amount, t_type))

# Commit e chiusura connessione
conn.commit()
conn.close()
print("Database popolato con successo!")
