# Run Development Version

!!! warning

    This is an unsecure development configuration.
        DO NOT USE IN PRODUCTION OR


To locally run stable not officially released version, simply

    docker run \
	 		--rm \
			-p 8000:8000 \
			-e ALLOWED_HOSTS="*" \
			-e DATABASE_URL="${DATABASE_URL}" \
			-e DEBUG="1" \
			-e SECRET_KEY=${SECRET_KEY} \
			-e SOCIAL_AUTH_REDIRECT_IS_HTTPS="False" \
			-e SUPERUSERS="admin," \
			saxix/booking:latest
