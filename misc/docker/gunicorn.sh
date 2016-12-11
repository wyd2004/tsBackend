#!/bin/bash

#source env/bin/activate
mkdir -p /var/log/gunicorn/
mkdir -p /var/log/supervisor/

exec gunicorn -c /data/misc/docker/gunicorn.conf tscast.wsgi:application
