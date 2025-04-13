from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import logging
import requests
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Di norma questa dovrebbe essere una chiave segreta casuale

# region Configurazioni (logging e db)
logging.basicConfig(
    filename="/var/log/http_honeypot_history.log",  # Ensure this path matches the volume mount
    level=logging.INFO,
    format="[%(asctime)s] - %(levelname)s - %(message)s",
)

@app.before_request
def log_request():
    logging.info(f"Request: {request.method} {request.path} - IP: {request.remote_addr}")

# Connessione al database SQLite
def get_db_connection():
    conn = sqlite3.connect("./database.db")
    conn.row_factory = sqlite3.Row
    return conn
# endregion

# region Endpoint vulnerabile a SQL Injection/XSS
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.args.get("q", "")
    conn = get_db_connection()
    cur = conn.cursor()

    sql_query = f"SELECT * FROM users WHERE id LIKE '{query}'"
    logging.info(f"Query eseguita: {sql_query}")  # LOG DELLA QUERY
    try:
        cur.execute(sql_query)  # VULNERABILE A SQLi
        results = cur.fetchall()
        conn.close()

        # Pass the results to the template
        return render_template('search_results.html', query=query, results=results)

    
    except Exception as e:
        logging.error(f"Errore: {e}")
        return f"Errore: {e}"
    
# Salva commenti
comments = []

# Pagina principale
@app.route("/", methods=["GET", "POST"])
def index():
    logging.info("Pagina principale visitata")  # Test log entry
    ip_address = request.remote_addr
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_telegram_message(f"Qualcuno ha visitato la pagina principale del sito!\nIP: {ip_address}, Timestamp: {timestamp}")  # Invia un messaggio Telegram
    if request.method == "POST":
        if 'username' in session:
            comment = request.form.get("comment", "")
            username = session['username']
            formatted_comment = f"{username}: {comment}"
            comments.append(formatted_comment)
            logging.info(f"New comment added: {formatted_comment}")
        else:
            return render_template("index.html", comments=comments, error="You can't comment without being logged in")
    return render_template("index.html", comments=comments)        
# endregion

# region Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check against the list of fake users
        users = [
            ("admin", "supersecret", "admin@example.com", "admin"),
            ("user1", "password123", "user1@example.com", "user"),
            ("guest", "guest123", "guest@example.com", "guest"),
            ("john_doe", "qwerty", "john@example.com", "user"),
            ("alice_smith", "letmein", "alice@example.com", "user")
        ]
        
        for user in users:
            if username == user[0] and password == user[1]:
                session['username'] = username
                return redirect(url_for('index'))
        return "Invalid credentials"
    return render_template("login.html")
# endregion

# region Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
# endregion

# region Messaggi Telegram
TELEGRAM_TOKEN = "7803238451:AAGFcmuAfredW4QALRMGmTnT7fTv6m8ohLQ" # non dimenticare di rimuovere
CHAT_ID = "6577743428" # Mettere il proprio chat id

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)
# endregion

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
