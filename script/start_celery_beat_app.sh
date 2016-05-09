#!/bin/bash

base_dir=$(cd "`dirname "$0"`"/..; pwd)

celery --workdir=${base_dir} --app=nwpc_monitor_task_scheduler.celery_server beat
