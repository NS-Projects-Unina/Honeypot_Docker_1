#!/bin/bash

# Logga i comandi eseguiti SENZA aggiungere il timestamp (lo aggiungerà lo script Python)
export PROMPT_COMMAND="echo \$(whoami):[\$(date '+%Y-%m-%d %H:%M:%S')] \$(history 1 | sed 's/^ *[0-9]* *//;s/^[0-9-]* [0-9:]* //') >> /var/log/ssh_honeypot_history.log"
export HISTFILE=/dev/null   # Evita che i comandi vengano scritti nel file di storia predefinito
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S "  # Puoi lasciare questo se vuoi, ma non serve per il timestamp

# Logga quando l'utente si disconnette
trap 'echo \$(whoami): User disconnected >> /var/log/ssh_honeypot_history.log' EXIT

# Avvia il comando bash
exec /bin/bash "$@"