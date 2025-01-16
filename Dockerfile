# Usa un'immagine base di Debian
FROM debian:bullseye

# Aggiorna i pacchetti e installa OpenSSH, rsyslog e Python
RUN apt-get update && \
    apt-get install -y openssh-server rsyslog python3 && \
    apt-get clean

# Crea una directory per l'host SSH e per i log
RUN mkdir /var/run/sshd && \
    mkdir -p /var/log/ssh && \
    chmod 755 /var/log/ssh

# Imposta la password di root
RUN echo 'root:pass' | chpasswd

# Configura OpenSSH
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config && \
    echo 'LogLevel VERBOSE' >> /etc/ssh/sshd_config && \
    echo 'SyslogFacility AUTH' >> /etc/ssh/sshd_config && \
    echo 'ForceCommand /usr/local/bin/bash_wrapper' >> /etc/ssh/sshd_config && \
    echo 'Banner /etc/ssh/banner.txt' >> /etc/ssh/sshd_config

# Configura il file di log condiviso per la cronologia
RUN touch /var/log/ssh_honeypot_history.log && \
    chmod 666 /var/log/ssh_honeypot_history.log && \
    chown root:root /var/log/ssh_honeypot_history.log

# Copia il wrapper bash nel container
COPY ./config/ssh/bash_wrapper.sh /usr/local/bin/bash_wrapper

# Assicurati che sia eseguibile
RUN chmod +x /usr/local/bin/bash_wrapper

# Aggiungi utenti di esempio
RUN useradd -m admin1 && echo "admin1:pass1" | chpasswd

# Configura Rsyslog per catturare gli eventi di autenticazione SSH
RUN echo 'auth.* /var/log/ssh/ssh.log' >> /etc/rsyslog.conf && \
    touch /var/log/ssh/ssh.log && \
    chmod 666 /var/log/ssh/ssh.log

# Aggiungi un filtro personalizzato per Rsyslog
RUN echo ':msg, contains, "lastlog_openseek" stop' >> /etc/rsyslog.d/ssh_filter.conf && \
    echo ':msg, contains, "Connection from" stop' >> /etc/rsyslog.d/ssh_filter.conf && \
    echo ':msg, contains, "Disconnected from user" stop' >> /etc/rsyslog.d/ssh_filter.conf && \
    echo ':msg, contains, "Received disconnect" stop' >> /etc/rsyslog.d/ssh_filter.conf

# Script Python per registrare connessioni e disconnessioni
RUN echo '#!/usr/bin/env python3' > /usr/local/bin/monitor_ssh.py && \
    echo 'import time' >> /usr/local/bin/monitor_ssh.py && \
    echo 'import re' >> /usr/local/bin/monitor_ssh.py && \
    echo 'log_file = "/var/log/ssh/ssh.log"' >> /usr/local/bin/monitor_ssh.py && \
    echo 'output_file = "/var/log/ssh_honeypot_history.log"' >> /usr/local/bin/monitor_ssh.py && \
    echo 'connection_pattern = re.compile(r".*Accepted password for (\\w+).*")' >> /usr/local/bin/monitor_ssh.py && \
    echo 'disconnection_pattern = re.compile(r".*Close session: user (\\w+).*")' >> /usr/local/bin/monitor_ssh.py && \
    echo 'with open(log_file, "r") as log, open(output_file, "a") as out:' >> /usr/local/bin/monitor_ssh.py && \
    echo '    log.seek(0, 2)' >> /usr/local/bin/monitor_ssh.py && \
    echo '    while True:' >> /usr/local/bin/monitor_ssh.py && \
    echo '        line = log.readline()' >> /usr/local/bin/monitor_ssh.py && \
    echo '        if not line:' >> /usr/local/bin/monitor_ssh.py && \
    echo '            time.sleep(1)' >> /usr/local/bin/monitor_ssh.py && \
    echo '            continue' >> /usr/local/bin/monitor_ssh.py && \
    echo '        connection = connection_pattern.search(line)' >> /usr/local/bin/monitor_ssh.py && \
    echo '        disconnection = disconnection_pattern.search(line)' >> /usr/local/bin/monitor_ssh.py && \
    echo '        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())' >> /usr/local/bin/monitor_ssh.py && \
    echo '        if connection:' >> /usr/local/bin/monitor_ssh.py && \
    echo '            user = connection.group(1)' >> /usr/local/bin/monitor_ssh.py && \
    echo '            user_port_match = re.search(r"port (\\d+)", line)' >> /usr/local/bin/monitor_ssh.py && \
    echo '            user_port = user_port_match.group(1) if user_port_match else "unknown"' >> /usr/local/bin/monitor_ssh.py && \
    echo '            user_ip_match = re.search(r"from (\\d+\\.\\d+\\.\\d+\\.\\d+)", line)' >> /usr/local/bin/monitor_ssh.py && \
    echo '            user_ip = user_ip_match.group(1) if user_ip_match else "unknown"' >> /usr/local/bin/monitor_ssh.py && \
    echo '            out.write(f"{user}:{timestamp} User connected, IP({user_ip}), Port({user_port})\\n")' >> /usr/local/bin/monitor_ssh.py && \
    echo '            out.flush()' >> /usr/local/bin/monitor_ssh.py && \
    echo '        if disconnection:' >> /usr/local/bin/monitor_ssh.py && \
    echo '            user = disconnection.group(1)' >> /usr/local/bin/monitor_ssh.py && \
    echo '            user_port_match = re.search(r"port (\\d+)", line)' >> /usr/local/bin/monitor_ssh.py && \
    echo '            user_port = user_port_match.group(1) if user_port_match else "unknown"' >> /usr/local/bin/monitor_ssh.py && \
    echo '            user_ip_match = re.search(r"from (\\d+\\.\\d+\\.\\d+\\.\\d+)", line)' >> /usr/local/bin/monitor_ssh.py && \
    echo '            user_ip = user_ip_match.group(1) if user_ip_match else "unknown"' >> /usr/local/bin/monitor_ssh.py && \
    echo '            out.write(f"{user}:{timestamp} User disconnected, IP({user_ip}), Port({user_port})\\n")' >> /usr/local/bin/monitor_ssh.py && \
    echo '            out.flush()' >> /usr/local/bin/monitor_ssh.py && \
    chmod +x /usr/local/bin/monitor_ssh.py

# Configura l'avvio automatico di Rsyslog, SSH e monitor_ssh.py
CMD touch /var/log/ssh_honeypot_history.log && \
chmod 666 /var/log/ssh_honeypot_history.log && \
chown root:root /var/log/ssh_honeypot_history.log && service rsyslog start && /usr/sbin/sshd && python3 /usr/local/bin/monitor_ssh.py
