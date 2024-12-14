#!/bin/sh -e


export MEDIA_ROOT="${MEDIA_ROOT:-/var/run/app/media}"
export STATIC_ROOT="${STATIC_ROOT:-/var/run/app/static}"
export UWSGI_PROCESSES="${UWSGI_PROCESSES:-"4"}"
export DJANGO_SETTINGS_MODULE="booking.config.settings"

case "$1" in
    run)
      django-admin migrate
      django-admin collectstatic
	    set -- tini -- "$@"
	    MAPPING=""
	    if [ "${STATIC_URL}" = "/static/" ]; then
	      MAPPING="--static-map ${STATIC_URL}=${STATIC_ROOT}"
	    fi
      set -- tini -- "$@"
	    set -- uwsgi --http :8000 \
	          --module booking.config.wsgi \
	          --mimefile=/conf/mime.types \
	          --uid user \
	          --gid booking \
            --buffer-size 8192 \
            --http-buffer-size 8192 \
	          $MAPPING
	    ;;
esac

exec "$@"
