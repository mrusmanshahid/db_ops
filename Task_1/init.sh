#!/bin/bash

sudo crontab -l > expansion_cron

sudo echo '@reboot source /etc/resize.sh > /var/log/expansion_cron_logs' >> expansion_cron

sudo crontab expansion_cron

sudo rm expansion_cron
