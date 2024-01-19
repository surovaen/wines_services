#!/bin/sh

python "manage.py" migrate --noinput

python "manage.py" collectstatic --noinput

python "manage.py" setup_periodic_tasks

gunicorn -c "$PROJECT_ROOT/gunicorn.conf.py" server.wsgi:application
