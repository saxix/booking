# Come Contribuire


Installare [uv](https://docs.astral.sh/uv/getting-started/installation/)

1. Clonare il repository e creare un virtualenv:

    git clone https://github.com/saxix/booking
    cd booking
    uv venv .venv --python 3.12
    source .venv/bin/activate
    uv sync --all-extras
    pre-commit install --hook-type pre-commit --hook-type pre-push

1. Configurare l’ambiente:


     export DATABASE_URL=sqlite:///booking.db
     export SECRET_KEY="super_secret_key_just_for_testing"
     export DEBUG=True
     export SUPERUSERS="admin@example.com,"  # can be a list
     export ADMIN_USER="admin@example.com"  # must be only one email
     export ADMIN_PASSWORD="password"

Se possiedi una chiave Google SSO e desideri abilitarla:

     export GOOGLE_CLIENT_ID= <
     export GOOGLE_CLIENT_SECRET=
     export SOCIAL_AUTH_REDIRECT_IS_HTTPS=False

Just want to run the app without installing source code? Use provided [Docker compose](Docker compose)

## Tailwind CSS (optional)

Questo progetto utilizza [django-tailwind](https://django-tailwind.readthedocs.io/en/latest/installation.html) per gestire i file CSS.
I sorgenti CSS si trovano nella directory  `booking/theme/static_src/src/`.

1. Configurare l’ambiente:

        export EXTRA_APPS="django_browser_reload"
        export EXTRA_MIDDLEWARES="django_browser_reload.middleware.BrowserReloadMiddleware,"

1.Installare le dipendenze Node.js:

        python manage.py tailwind install


1. Compilare il CSS finale:

        python manage.py tailwind build

    Oppure utilizzare la [modalità di sviluppo](https://django-tailwind.readthedocs.io/en/latest/usage.html#running-in-development-mode)

        python manage.py tailwind start

ALe modifiche ai file .scss attiveranno la compilazione del file .css e il browser ricaricherà automaticamente la pagina.

## Run tests

I test si trovano nella cartella `tests`. Per eseguirli, usa:

    pytest tests


## Avviare il server locale

Prima di eseguire l’applicazione, configura alcune variabili d’ambiente:

      export DATABASE_URL=sqlite://booking.db
      export SECRET_KEY="super_secret_key_just_for_testing"
      export DEBUG=True
      export SUPERUSERS=<your email>

!!! note

    Se preferisci utilizzare PostgreSQL, imposta DATABASE_URL come segue:

       `postgres://<username>:<password>@<ip>:<port>/<database>`


Se desideri abilitare Google SSO, aggiungi:

      export GOOGLE_CLIENT_ID=...
      export GOOGLE_CLIENT_SECRET=...
      export SOCIAL_AUTH_REDIRECT_IS_HTTPS=False

Infine esegui:


    python manage.py runserver

e apri il browser su http://localhost:8000


## Caricare dati di esempio

Per caricare dati demo, esegui:

    python manage.py demo


## Docker compose

n alternativa, puoi utilizzare il Docker Compose fornito per lo sviluppo.
Questa soluzione fa partire tutto il necessario,
e rende l'applicazione disponibile su https://localhost:8000

    docker compose up
