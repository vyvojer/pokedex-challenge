#!/bin/bash

./scripts/wait-for-it.sh $REDIS_HOST:$REDIS_PORT
./scripts/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT

celery -A pokedex.celery beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info
