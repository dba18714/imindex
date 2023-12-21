#!/bin/bash

# 启动 Celery Worker
celery -A mysite worker -l info &

# 启动 Gunicorn
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
