
i18n:  ## i18n support. Run makemessages and compilemessages
	cd src && django-admin makemessages --locale it_IT --settings=booking.config.settings --pythonpath=../src
	cd src && django-admin compilemessages --settings=booking.config.settings --pythonpath=../src
