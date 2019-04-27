#!/bin/bash
set -x

if [ ! -r custom.ini ]; then
    if [ -n "$REDIS_PASSWORD" ]; then
        REDIS_HOST="$REDIS_SERVICE_HOST:$REDIS_SERVICE_PORT"
        REDIS_URL="redis://:$REDIS_PASSWORD@$REDIS_HOST"
        sed -e "s;redis://.*;$REDIS_URL;" production.ini > custom.ini
    else
        cp development.ini custom.ini
    fi
fi

[ -n "$CONTAINER_DEBUG" ] && sleep 99999999

pserve custom.ini
