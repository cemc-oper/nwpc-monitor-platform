#!/usr/bin/env bash

base_dir=$(cd "`dirname "$0"`"/..; pwd)
export NWPC_MONITOR_PLATFORM_BASE=${base_dir}
export PYTHONPATH=${base_dir}:$PYTHONPATH

export MODE=develop

python3 ${NWPC_MONITOR_PLATFORM_BASE}/nwpc_monitor_task_scheduler/run.py \
    --config-file="../nmp_scheduler/conf/celery_server.develop.config.yaml" \
    beat
