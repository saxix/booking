---
title: Docker
---

## Compose

Source repository comes with a pre-configured Docker compose file. To use it just point to the root folder and type

    docker compose up

this will start all required components (Postgres, Redis, App).
You can navigate to http://localhost:8000 to check the application

!!! note

    Provided stack also create a supruser account `admin@example.com/password`

!!! warning

    Due to the fact this is only for testing purposes, provided compose does not use any volume, so no data are persisted.

## Dockerfile

To locally build your docker image just run:

    	DOCKER_BUILDKIT=1 docker build \
			--target dist \
			-t booking:local \
			-f docker/Dockerfile .
