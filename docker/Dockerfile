FROM python:3.12-slim-bookworm AS base_os

RUN set -x \
  && runtimeDeps=" \
    libmagic1 \
    libxml2 \
  " \
  && apt-get update && apt-get install -y --no-install-recommends ${runtimeDeps} \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && groupadd --gid 1024 booking \
    && adduser --disabled-login --disabled-password --no-create-home --ingroup booking -q user


# ------- builder -------
FROM base_os AS builder
RUN set -x \
    && buildDeps="build-essential \
cmake \
" \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN pip install uv uwsgi

# ------- tests -------
FROM builder AS tests
ARG BUILD_DATE
ARG GIT_SHA

LABEL distro="tests"

ENV PATH=/venv/bin:/usr/local/bin/:/usr/bin:/bin \
    DJANGO_SETTINGS_MODULE=booking.config.settings \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=""\
    VIRTUAL_ENV=/venv \
    UV_PROJECT_ENVIRONMENT=/venv \
    UWSGI_PROCESSES=4

WORKDIR /app
COPY uv.lock README.md MANIFEST.in pyproject.toml /app/
COPY src /app/src/

RUN --mount=type=cache,target=/root/.cache/,id=uvcache \
    find ../src -name 'node_modules' -prune \
        -o -name *.py -o -name *.html -o -name *.js -o -name *.css \
        -type f \
        -exec ls -l "{}" \;  | sha1sum | awk '{print $1}' > CODE_CHECKSUM \
    && uv sync --cache-dir=/root/.cache \
        --python=/usr/local/bin/python \
        --python-preference=system \
        --frozen

# ------- dipendenze di produzione -------
FROM builder AS production
ENV PATH=/venv/bin:/usr/local/bin/:/usr/bin:/bin \
    DJANGO_SETTINGS_MODULE=booking.config.settings \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=""\
    VIRTUAL_ENV=/venv \
    UV_PROJECT_ENVIRONMENT=/venv \
    UWSGI_PROCESSES=4


WORKDIR /app
COPY uv.lock README.md MANIFEST.in pyproject.toml /app/
COPY src /app/src/

RUN --mount=type=cache,target=/root/.cache/,id=uvcache \
    uv sync --cache-dir=/root/.cache \
        --python=/usr/local/bin/python \
        --python-preference=system \
        --no-dev --frozen



# ------- distribuzione finale -------
FROM base_os AS dist
ARG BUILD_DATE
ARG GIT_SHA
ARG BRANCH

ENV PATH=/venv/bin:/usr/local/bin/:/usr/bin:/bin \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=booking.config.settings \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=""\
    PGSSLCERT="/tmp/postgresql.crt" \
    UV_PROJECT_ENVIRONMENT=/venv \
    VIRTUAL_ENV=/venv


WORKDIR /app
COPY docker/conf /conf/
COPY docker/bin/* /usr/local/bin/
COPY LICENSE.md README.md /
COPY . /app/

COPY --chown=user:booking --from=production /venv /venv
COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/uv /usr/local/bin/

RUN --mount=type=cache,target=/root/.cache/,id=uvcache \
    uv --cache-dir=/root/.cache pip install --link-mode=copy  --no-deps . \
    && rm -fr /app/

EXPOSE 8000
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["run"]


LABEL maintainer="user@booking.org"
LABEL org.opencontainers.image.authors="user@booking.org"
LABEL org.opencontainers.image.description="Car Booking System"
