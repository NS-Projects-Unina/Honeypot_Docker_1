import time
import re

# Definisci il percorso del file di log SSH e il file di output dove verranno scritti i log elaborati
log_file = "/var/log/ssh/ssh.log"
output_file = "/var/log/ssh_honeypot_history.log"

# Compila le espressioni regolari per individuare i pattern di connessione e disconnessione nel file di log
connection_pattern = re.compile(r".*Accepted password for *")
disconnection_pattern = re.compile(r".*Close session: user *")

# Apri il file di log in modalità lettura e il file di output in modalità append
with open(log_file, "r") as log, open(output_file, "a") as out:
    # Sposta il puntatore del file alla fine del file di log per iniziare a monitorare le nuove voci
    log.seek(0, 2)
    
    while True:
        # Leggi una nuova riga dal file di log
        line = log.readline()
        
        # Se non ci sono nuove righe disponibili, attendi 1 secondo e continua
        if not line:
            time.sleep(1)
            continue
        
        # Controlla se la riga corrisponde al pattern di connessione
        connection = connection_pattern.search(line)
        # Controlla se la riga corrisponde al pattern di disconnessione
        disconnection = disconnection_pattern.search(line)
        
        # Ottieni il timestamp corrente nel formato specificato
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
        
        if connection:
            # Estrai il nome utente dal log di connessione
            user = connection.group(1)
            # Estrai il numero di porta dalla riga di log, se disponibile
            user_port_match = re.search(r"port (\\d+)", line)
            user_port = user_port_match.group(1) if user_port_match else "unknown"
            # Estrai l'indirizzo IP dalla riga di log, se disponibile
            user_ip_match = re.search(r"from (\\d+\\.\\d+\\.\\d+\\.\\d+)", line)
            user_ip = user_ip_match.group(1) if user_ip_match else "unknown"
            # Scrivi i dettagli della connessione nel file di output
            out.write(f"{user}:{timestamp} User connected, IP({user_ip}), Port({user_port})\\n")
            out.flush()  # Assicurati che i dati vengano scritti immediatamente nel file
        
        if disconnection:
            # Estrai il nome utente dal log di disconnessione
            user = disconnection.group(1)
            # Estrai il numero di porta dalla riga di log, se disponibile
            user_port_match = re.search(r"port (\\d+)", line)
            user_port = user_port_match.group(1) if user_port_match else "unknown"
            # Estrai l'indirizzo IP dalla riga di log, se disponibile
            user_ip_match = re.search(r"from (\\d+\\.\\d+\\.\\d+\\.\\d+)", line)
            user_ip = user_ip_match.group(1) if user_ip_match else "unknown"
            # Scrivi i dettagli della disconnessione nel file di output
            out.write(f"{user}:{timestamp} User disconnected, IP({user_ip}), Port({user_port})\\n")
            out.flush()  # Assicurati che i dati vengano scritti immediatamente nel file