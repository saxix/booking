# Contributing


Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

1. Clone the repo and create virtualenv

    git clone https://github.com/saxix/booking
    cd booking
    uv venv .venv --python 3.12
    source .venv/bin/activate
    uv sync --all-extras
    pre-commit install --hook-type pre-commit --hook-type pre-push

1. Configure your environment:


     export DATABASE_URL=sqlite:///booking.db
     export SECRET_KEY="super_secret_key_just_for_testing"
     export DEBUG=True
     export SUPERUSERS="admin@example.com,"  # can be a list
     export ADMION_USER="admin@example.com"  # must be only one email
     export ADMION_PASSWORD="password"

If you have a google SSO key and you want to enable it:

     export GOOGLE_CLIENT_ID=
     export GOOGLE_CLIENT_SECRET=
     export SOCIAL_AUTH_REDIRECT_IS_HTTPS=False

Just want to run the app without installing source code? Use provided [Docker compose](Docker compose)

## Tailwind CSS (optional)

This project uses [django-tailwind](https://django-tailwind.readthedocs.io/en/latest/installation.html) to manage
CSS. CSS sources are located in the `booking/theme/static_src/src/`.
If you need to edit the CSS follow the below steps:

1. Configure the enviroment

        export EXTRA_APPS="django_browser_reload"
        export EXTRA_MIDDLEWARES="django_browser_reload.middleware.BrowserReloadMiddleware,"

1. Install node dependencies

        python manage.py tailwind install


1. Build the final CSS

        python manage.py tailwind build

    Or you can run the [development mode](https://django-tailwind.readthedocs.io/en/latest/usage.html#running-in-development-mode)

        python manage.py tailwind start

Any changes to the .scss will trigger the .css compilation, followed by the browser reloading the page.
Any changes to any other file will trigger the browser page reload.


## Run tests

Tests are located in the `tests` folder. To run them just type

    pytest tests


## Run local server

Before you can run the sample application you should set some environment variables:

      export DATABASE_URL=sqlite://booking.db
      export SECRET_KEY="super_secret_key_just_for_testing"
      export DEBUG=True
      export SUPERUSERS=<your email>

!!! note

    In case you prefer to use PostgreSQL you can set `DATABASE_URL` as

       `postgres://<username>:<password>@<ip>:<port>/<database>`


if you want to enable Google SSO you should add:

      export GOOGLE_CLIENT_ID=...
      export GOOGLE_CLIENT_SECRET=...
      export SOCIAL_AUTH_REDIRECT_IS_HTTPS=False

later you can


    python manage.py runserver

and point your browser to http://localhost:8000

## Load sample data

    python manage.py demo


## Docker compose

Alternatively you can use provided docker compose for development

    docker compose up

Alternatively you can use provided docker compose for development

    docker compose up
