import os
import subprocess
import time

# Nome del container Docker da cui copiare i log
container_name = "ssh_logger"  # Modifica con il nome del tuo container

# Percorsi di origine e destinazione
source_path = "/var/log/ssh_honeypot_history_copy.log"
destination_path = os.path.join(os.getcwd(), "logs\\ssh_honeypot_history.log")

# Funzione per copiare il file dal container
def copy_log_from_container():
    # Usa il comando Docker per copiare il file dal container
    try:
        subprocess.run(["docker", "cp", f"{container_name}:{source_path}", destination_path], check=True)
        print(f"Log copiato con successo in {destination_path}")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante la copia del file: {e}")

if __name__ == "__main__":

    while True:
        copy_log_from_container()
        # Copia il file ogni 3 secondi
        time.sleep(3)
