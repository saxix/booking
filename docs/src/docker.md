---
title: Docker
---

## Compose

Il repository dei sorgenti è dotato di un file Docker compose preconfigurato.
Per utilizzarlo, basta puntare alla cartella principale e digitare

    docker compose up

tquesto avvierà tutti i componenti richiesti (Postgres, Redis, App).

Puoi andare su http://localhost:8000 per controllare l'applicazione


!!! note

    Lo stack fornito crea anche un account superutente `admin@example.com/password`


!!! warning

    Poiché questo è solo per scopi di test, lo stack non utilizza alcun volume,
    tutti i datoi andranno persi alla chiusura dello stack.

## Dockerfile

Per creare localmente la tua immagine docker, esegui semplicemente:

    	export DOCKER_BUILDKIT=1
        docker build --target dist --build-arg BUILDKIT_INLINE_CACHE=1 --cache-from saxix/booking:latest -t booking:local -f docker/Dockerfile .
