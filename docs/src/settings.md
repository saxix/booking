# Variabili di Ambiente


Di seguito sono elencate le variabili di ambiente che è possibile configurare.


### ADMIN_PASSWORD

Se impostata (insieme a `ADMIN_USER`) sarà usata come password iniziale dell'amministratore

### ADMIN_USER

Se nessun amministratore è presente nel database, e questa variabile è impostata, verrà creato
un utente amministratore con questo username/email e `ADMIN_PASSWORD`  come password:

!!! note

    Devono essere impostate entrambe


DATABASE_URL=sqlite:///booking.db
DEBUG=True
EXTRA_APPS="django_browser_reload"
EXTRA_MIDDLEWARES="django_browser_reload.middleware.BrowserReloadMiddleware,"
GOOGLE_CLIENT_ID= <
GOOGLE_CLIENT_SECRET=
SECRET_KEY="super_secret_key_just_for_testing"
SOCIAL_AUTH_REDIRECT_IS_HTTPS=False
SUPERUSERS="admin@example.com,"  # elenco
