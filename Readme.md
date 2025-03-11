# Progetto Honeypot Docker
Questo progetto consiste in due honeypot: un honeypot HTTP e un honeypot SSH. Lo scopo di questi honeypot è attirare e registrare attività dannose per scopi di analisi e ricerca.

## Honeypot HTTP

### Descrizione
L'honeypot HTTP è un'applicazione web Flask che simula un servizio web vulnerabile. Include endpoint che sono intenzionalmente vulnerabili agli attacchi di SQL injection e XSS. L'applicazione registra tutte le richieste in arrivo e le memorizza in un file di log.

### Configurazione
1. Buildare ed eseguire il container Docker
2. Eseguire il file init_db.py per inizializzare un db di prova
3. L'applicazione web sarà disponibile su http://localhost:5000

### Endpoints
/: Pagina principale con una sezione commenti e un modulo di ricerca, vulnerabile ad RCE.
/search: Endpoint vulnerabile a SQL injection.

### Logging
I log sono memorizzati in logs/http_honeypot_history_copy.log sulla macchina host.

## Honeypot SSH

### Descrizione
L'honeypot SSH simula un server SSH vulnerabile. Registra tutte le connessioni SSH e i comandi eseguiti dall'attaccante. I log sono memorizzati in un volume condiviso e copiati in una posizione sicura per prevenire manomissioni.

### Configurazione
1. Buildare ed eseguire il container Docker
2. Il server SSH sarà disponibile al collegamento sul porto 2222, sono presenti 2 utenti preimpostati, root|pass e admin1|pass1

### Logging
I log sono memorizzati in secure_logs/ssh_honeypot_history_copy.log sulla macchina host.

## Misure di Sicurezza
File system in sola lettura: Il file system del container dell'honeypot HTTP è impostato in sola lettura per prevenire modifiche al codice.

Copia dei log: I log sono copiati in una posizione sicura per prevenire manomissioni da parte degli attaccanti.
