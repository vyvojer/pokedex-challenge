#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput
gunicorn pokedex.wsgi:application --bind 0.0.0.0:8000