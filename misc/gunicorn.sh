#!/bin/bash

#source env/bin/activate

exec gunicorn -c misc/gunicorn.conf tscast.wsgi:application
