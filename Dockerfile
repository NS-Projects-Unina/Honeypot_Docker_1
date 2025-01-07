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

# Copia lo script di creazione degli utenti, va creato uno script che legga il file users.txt e crei gli utenti
COPY /config/ssh/users.txt /etc/ssh/users.txt

# Crea admin e imposta la password
RUN useradd -m admin && echo "admin:pass" | chpasswd

# Imposta il comando per avviare il server SSH
CMD ["/usr/sbin/sshd", "-D"]
