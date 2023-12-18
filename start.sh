#!/bin/bash
service cron restart
tail -f /var/log/cron.log
