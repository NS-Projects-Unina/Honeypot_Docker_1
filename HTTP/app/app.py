from flask import Flask, request, render_template
import sqlite3
import logging

app = Flask(__name__)

# Configura il logging su file
logging.basicConfig(
    filename="/var/log/http_honeypot_history.log",  # Ensure this path matches the volume mount
    level=logging.INFO,
    format="[%(asctime)s] - %(levelname)s - %(message)s",
)

@app.before_request
def log_request():
    logging.info(f"Request: {request.method} {request.path} - IP: {request.remote_addr} - Data: {request.data}")

# Connessione al database SQLite
def get_db_connection():
    conn = sqlite3.connect("./database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint vulnerabile a SQL Injection
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.args.get("q", "")
    conn = get_db_connection()
    cur = conn.cursor()

    sql_query = f"SELECT * FROM users WHERE username LIKE '{query}'"
    logging.info(f"Query eseguita: {sql_query}")  # LOG DELLA QUERY
    try:
        cur.execute(sql_query)  # VULNERABILE A SQLi
        results = cur.fetchall()
        logging.info(f"Risultato query: {results}")

        conn.close()

        # Pass the results to the template
        return render_template('search_results.html', query=query, results=results)

    
    except Exception as e:
        logging.error(f"Errore: {e}")
        return f"Errore: {e}"
    

# Store comments in memory (not in a database)
comments = []

# Pagina principale
@app.route("/", methods=["GET", "POST"])
def index():
    logging.info("Index page accessed")  # Test log entry
    if request.method == "POST":
        comment = request.form.get("comment", "")
        comments.append(comment)
        logging.info(f"New comment added: {comment}")
        
    return render_template("index.html", comments=comments)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
