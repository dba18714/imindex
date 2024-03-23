#!/bin/bash

python manage.py compilemessages &&
python manage.py collectstatic --noinput &&
_for_deploy/wait-for-db.sh db &&
# service cron start &&
python manage.py migrate &&
python manage.py imindex_install &&
python manage.py runserver 0.0.0.0:8000
