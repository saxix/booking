---
title: Esecuzione
---

E' possibile lanciare l'applicazione in diverse modalità:

## Compose (stable)

Il repository dei sorgenti è dotato di un file Docker compose preconfigurato.
Per utilizzarlo, basta puntare alla cartella principale e digitare

    docker compose up

questo avvierà tutti i componenti richiesti (Postgres, Redis, App).
L'applicazione partirà usando l'ultima versione stabile disponibile su https://hub.docker.com/repository/docker/saxix/booking/tags

Puoi andare su http://localhost:8000 per controllare l'applicazione


!!! note

    Lo stack fornito crea anche un account superutente `admin@example.com/password`


!!! warning

    Poiché questo è solo per scopi di test, lo stack non utilizza alcun volume,
    tutti i datoi andranno persi alla chiusura dello stack.


## Compose (development)

Questa modalità esegue il compose in modalità sviluppo, utilizzando il codice locale per
eseguire la build della docker in modalità `watch` (https://docs.docker.com/compose/how-tos/file-watch/).


    docker compose --profile dev watch


## Virtualenv

Dopo aver scaricato  [uv](https://docs.astral.sh/uv/getting-started/installation/), è necessario configurare qualche variabila di ambiente

    DATABASE_URL=

    uv sync
    uv run python manage.py migrate
    uv run python manage.py runserver


## Dockerfile

Per creare localmente la tua immagine docker, esegui semplicemente:

    	export DOCKER_BUILDKIT=1
        docker build --target dist --build-arg BUILDKIT_INLINE_CACHE=1 --cache-from saxix/booking:latest -t booking:local -f docker/Dockerfile .
