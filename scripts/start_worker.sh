#!/bin/bash

./scripts/wait-for-it.sh $REDIS_HOST:$REDIS_PORT
./scripts/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT


: ${WORKER_CONCURRENCY:=4}
: ${POOL:="prefork"}


celery -A pokedex.celery worker -E --loglevel=info --pool=$POOL --concurrency=$WORKER_CONCURRENCY
