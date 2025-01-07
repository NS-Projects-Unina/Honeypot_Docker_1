#!/bin/bash
echo "Starting monitor script..."

# Verifica la data e l'ora nel contenitore
date

# Verifica se i file di log sono raggiungibili
ls -l /var/log/ssh_honeypot.log

# Aggiungi un messaggio di log
echo "[INFO] Monitoring user activity..." >> /var/log/ssh_honeypot.log

# Altri comandi di monitoraggio ????

