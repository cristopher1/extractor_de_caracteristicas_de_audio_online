#!/bin/bash

if [ "$DJANGO_ENVIRONMENT" = "development" ]
then
    python manage.py makemigrations && \
    python manage.py migrate
fi

exec "$@"
