#!/bin/bash
set -x

if [ -n "$REDIS_PASSWORD" ]; then
    REDIS_HOST="$REDIS_SERVICE_HOST:$REDIS_SERVICE_PORT"
    REDIS_URL="redis://:$REDIS_PASSWORD@$REDIS_HOST"
    sed -e "s;redis://.*;$REDIS_URL;" production.ini > custom.ini
    pserve custom.ini
else
    pserve development.ini
fi
