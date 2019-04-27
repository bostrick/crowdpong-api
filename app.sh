#!/bin/bash
set -x

F=development.ini

if [ -n "$REDIS_password" ]; then
    REDIS_HOST="$REDIS_SERVICE_HOST:$REDIS_SERVICE_PORT"
    REDIS_URL="redis://:$REDIS_password@$REDIS_HOST"
    sed -e "s;redis://.*;$REDIS_URL;" $F > custom.ini
    pserve custom.ini
else
    pserve development.ini
fi
