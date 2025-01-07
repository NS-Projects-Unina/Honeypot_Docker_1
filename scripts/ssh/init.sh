#!/bin/bash

# Verifica che il file users.txt esista
if [ ! -f /etc/ssh/users.txt ]; then
    echo "Il file users.txt non è stato trovato!"
    exit 1
fi

# Leggi il file users.txt e crea gli utenti
while IFS=: read -r username password; do
    # Aggiungi l'utente
    useradd -m "$username"
    
    # Imposta la password per l'utente
    echo "$username:$password" | chpasswd

    # Concedi permessi sudo senza password
    echo "$username ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
done < /etc/ssh/users.txt

echo "Gli utenti sono stati creati con successo!"
