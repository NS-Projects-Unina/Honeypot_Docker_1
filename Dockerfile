# Usa un'immagine base di Debian
FROM debian:bullseye

# Imposta l'autore
LABEL maintainer="Ciccio@Bello.com"

# Aggiorna i pacchetti e installa OpenSSH
RUN apt-get update && \
    apt-get install -y openssh-server && \
    apt-get clean

# Crea una directory per l'host SSH
RUN mkdir /var/run/sshd

# Copia il file di configurazione SSH personalizzato
COPY /config/ssh/sshd_config /etc/ssh/sshd_config

# Copia il banner SSH
COPY /config/ssh/ssh_banner /etc/ssh/ssh_banner

# Copia lo script di creazione degli utenti
COPY /config/ssh/users.txt /etc/ssh/users.txt

## SEZIONE LOGGING
# Crea il file di log
#RUN touch /var/log/ssh_honeypot.log && chown root:root /var/log/ssh_honeypot.log

# Copia lo script di monitoraggio
#COPY scripts/ssh/monitor_user_activity.sh /usr/local/bin/monitor_user_activity.sh

# Rendi lo script eseguibile
#RUN chmod +x /usr/local/bin/monitor_user_activity.sh

# Avvia lo script di monitoraggio quando un utente accede via SSH
#ENTRYPOINT ["/usr/local/bin/monitor_user_activity.sh"]
## FINE SEZIONE LOGGING

# Crea gli utenti a partire dal file users.txt (non funziona)
RUN while IFS=: read -r user pass; do \
    if ! useradd -m "$user"; then \
        exit 1; \
    fi; \
    if ! echo "$user:$pass" | chpasswd; then \
        exit 1; \
    fi; \
done < /etc/ssh/users.txt

RUN useradd -m admin1 && echo "admin1:pass1" | chpasswd
# Imposta il comando per avviare il server SSH
CMD ["/usr/sbin/sshd", "-D"]