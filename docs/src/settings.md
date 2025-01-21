# Variabili di Ambiente


Di seguito sono elencate le variabili di ambiente che è possibile configurare.


### ADMIN_PASSWORD

Se impostata (insieme a `ADMIN_USER`) sarà usata come password iniziale dell'amministratore

### ADMIN_USER

Se nessun amministratore è presente nel database, e questa variabile è impostata, verrà creato
un utente amministratore con questo username/email e `ADMIN_PASSWORD`  come password:

!!! note

    Devono essere impostate entrambe


### DATABASE_URL

Stringa di connessione in formato URI. Es

    postgres://username:password@127.0.0.1:5432/booking

### DEBUG

Abilita o meno il debug mode

EXTRA_APPS="django_browser_reload"
EXTRA_MIDDLEWARES="django_browser_reload.middleware.BrowserReloadMiddleware,"


### GOOGLE_CLIENT_ID

Google client ID per abilitare il SSO



### GOOGLE_CLIENT_SECRET

Google secret key per SSO

!!! Note:

    `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` devono essere entrambe impostate


### SECRET_KEY

Chiave di sicurezza.

!!! danger

    In ambiente di produzione questo valore non deve essere condiviso

### SOCIAL_AUTH_REDIRECT_IS_HTTPS

Impostare a `true` solo se si usa SSO e si esegue l'applicazione in HTTPS

### SUPERUSERS

Elenco di email corrispondenti ad utenti che verrano automaticamente creati come amministratori al primo login.

!!! note

    Se lo user esiste e non è amministratore NON verra cambiato.
    Questo permette ad esempio di impostare il devops come amministratore
    durante la fase di setup, ma di disabilitarlo subito dopo.
