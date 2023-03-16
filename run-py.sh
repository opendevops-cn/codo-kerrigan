#!/usr/bin/env bash
sleep 1
SERVICE_NAME=`echo $1|cut -d- -f2-`
cd /data && python3 startup.py --service=${SERVICE_NAME}