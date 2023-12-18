#!/bin/bash

service cron start
tail -f /code/logs/cron.log
