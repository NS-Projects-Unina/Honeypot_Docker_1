import re
from datetime import datetime

# Percorsi dei file
auth_log_path = "./logs/auth.log"
history_log_path = "./logs/ssh_honeypot_history"
combined_log_path = "./logs/combined.log"

# Funzione per convertire una stringa di data in un oggetto datetime
def parse_auth_log_timestamp(line):
    try:
        return datetime.strptime(line[:15], "%b %d %H:%M:%S")
    except ValueError:
        return None

# Leggi e analizza il file auth.log
def parse_auth_log(file_path):
    with open(file_path, "r") as f:
        auth_logs = []
        for line in f:
            timestamp = parse_auth_log_timestamp(line)
            if timestamp:
                auth_logs.append((timestamp, line.strip()))
        return auth_logs

# Leggi e analizza il file ssh_honeypot_history
def parse_history_log(file_path):
    with open(file_path, "r") as f:
        history_logs = []
        for line in f:
            line = line.strip()
            # Controlla se la linea rappresenta un timestamp o un comando
            if line.startswith("#"):
                timestamp = datetime.fromtimestamp(int(line[1:]))
                history_logs.append((timestamp, None))  # None per marcare un cambio di utente
            elif line:
                history_logs.append((None, line))  # Nessun timestamp, solo il comando
        return history_logs

# Unione e scrittura dei log combinati
def combine_logs(auth_logs, history_logs, output_path):
    with open(output_path, "w") as f:
        i, j = 0, 0
        while i < len(auth_logs) or j < len(history_logs):
            auth_time = auth_logs[i][0] if i < len(auth_logs) else None
            history_time = history_logs[j][0] if j < len(history_logs) and history_logs[j][0] else None

            # Decidi quale log scrivere in base alla sequenza temporale
            if auth_time and (not history_time or auth_time <= history_time):
                f.write(auth_logs[i][1] + "\n")
                i += 1
            elif history_time:
                if history_logs[j][1] is None:
                    f.write(f"# Non-root command session started at {history_time}\n")
                else:
                    f.write(history_logs[j][1] + "\n")
                j += 1
            else:
                break

# Esegui il processo
if __name__ == "__main__":
    auth_logs = parse_auth_log(auth_log_path)
    history_logs = parse_history_log(history_log_path)
    combine_logs(auth_logs, history_logs, combined_log_path)
    print(f"Log combinato creato: {combined_log_path}")
