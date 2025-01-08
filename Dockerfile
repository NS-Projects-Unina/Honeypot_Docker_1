# Usa un'immagine base di Debian
FROM debian:bullseye

# Imposta l'autore
LABEL maintainer="Ciccio@Bello.com"

# Aggiorna i pacchetti e installa OpenSSH e rsyslog
RUN apt-get update && \
    apt-get install -y openssh-server rsyslog && \
    apt-get clean

# Crea una directory per l'host SSH
RUN mkdir /var/run/sshd

# Crea la directory per i log
RUN mkdir -p /var/log/ssh

# Copia il file di configurazione SSH personalizzato
COPY /config/ssh/sshd_config /etc/ssh/sshd_config

# Copia il banner SSH
COPY /config/ssh/ssh_banner /etc/ssh/ssh_banner

# Copia lo script di creazione degli utenti
COPY /config/ssh/users.txt /etc/ssh/users.txt

# Aggiungi utenti di esempio
RUN useradd -m admin1 && echo "admin1:pass1" | chpasswd

# Imposta rsyslog per avviarsi automaticamente
RUN systemctl enable rsyslog

# Imposta il comando per avviare rsyslog e SSH
CMD service rsyslog start && /usr/sbin/sshd -D
