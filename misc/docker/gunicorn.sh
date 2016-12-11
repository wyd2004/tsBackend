#!/bin/bash

#source env/bin/activate
mkdir -p /var/log/gunicorn/
mkdir -p /var/log/supervisor/

exec gunicorn -c misc/gunicorn.conf tscast.wsgi:application
