#!/bin/sh -e


export MEDIA_ROOT="/var/run/app/media"
export STATIC_ROOT="/var/run/app/static"
export DJANGO_SETTINGS_MODULE="booking.config.settings"
mkdir -p ${STATIC_ROOT}

case "$1" in
    run)
      django-admin migrate --no-input
      django-admin collectstatic --no-input
      set -- tini -- "$@"
	    set -- uwsgi --http :8000 \
	          -H /app/.venv \
	          --module booking.config.wsgi \
	          --mimefile=/conf/mime.types \
	          --uid user \
	          --gid booking \
            --buffer-size 8192 \
            --http-buffer-size 8192 \
	          --static-map "/static/=${STATIC_ROOT}"
	    ;;
esac

exec "$@"
