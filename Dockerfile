# Usa un'immagine base di Debian
FROM debian:bullseye

# Aggiorna i pacchetti e installa OpenSSH e rsyslog
RUN apt-get update && \
    apt-get install -y openssh-server rsyslog && \
    apt-get clean

# Crea una directory per l'host SSH
RUN mkdir /var/run/sshd

# Crea la directory per i log
RUN mkdir -p /var/log/ssh

# Imposta la password di root
RUN echo 'root:pass' | chpasswd

# Modifica la configurazione di OpenSSH
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
RUN echo 'LogLevel VERBOSE' >> /etc/ssh/sshd_config
RUN echo 'SyslogFacility AUTH' >> /etc/ssh/sshd_config
RUN echo 'Banner /etc/ssh/banner.txt' >> /etc/ssh/sshd_config

# Create a shared history file for all users
RUN touch /var/log/ssh_honeypot_history && chmod 666 /var/log/ssh_honeypot_history

# Configure the global bashrc to log commands for all users
RUN echo 'PROMPT_COMMAND="history -a; history -n"' >> /etc/bash.bashrc
RUN echo 'HISTFILE=/var/log/ssh_honeypot_history' >> /etc/bash.bashrc
RUN echo 'HISTSIZE=10000' >> /etc/bash.bashrc
RUN echo 'HISTFILESIZE=20000' >> /etc/bash.bashrc
RUN echo 'HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S "' >> /etc/bash.bashrc

# Aggiungi utenti di esempio
RUN useradd -m admin1 && echo "admin1:pass1" | chpasswd

# Imposta rsyslog per avviarsi automaticamente
RUN systemctl enable rsyslog

# Imposta il comando per avviare rsyslog e SSH
CMD service rsyslog start && /usr/sbin/sshd -D