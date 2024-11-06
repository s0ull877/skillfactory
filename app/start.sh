#!/bin/bash

sleep 5
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py create_superuser

gunicorn app.wsgi:application --bind 0:8000

