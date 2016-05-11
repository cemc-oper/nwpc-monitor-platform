#!/bin/bash

base_dir=$(cd "`dirname "$0"`"/..; pwd)
#export NWPC_MONITOR_PLATFORM_BASE=${base_dir}

celery --workdir=${base_dir} --app=nwpc_monitor_task_scheduler.celery_server -l info worker -B -s /tmp/celerybeat-schedule
