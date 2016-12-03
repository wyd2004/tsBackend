#!/bin/bash

source env/bin/activate

mkdir  -p /var/log/gunicorn/

cd src/tscast

exec gunicorn -k gevent tscast.wsgi:application \
    --env TSCAST_ENV=PRODUCT \ 
    --name mjtt_django \
    --bind 127.0.0.1:4001 \
    --workers 3 \
    --log-level=info \
    --log-file=/var/log/gunicorn/gunicorn.log \
    --access-logfile=/var/log/gunicorn/access.log \
    "$@"
