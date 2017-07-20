#!/usr/bin/env bash

export NWPC_MONITOR_PLATFORM_BASE=$(cd "`dirname "$0"`"/..; pwd)
export PYTHONPATH=${NWPC_MONITOR_PLATFORM_BASE}:$PYTHONPATH

python3 ${NWPC_MONITOR_PLATFORM_BASE}/nwpc_monitor_task_scheduler/run.py \
    --config-file="../nwpc_monitor_task_scheduler/conf/celery_server.develop.config.yaml" \
    worker
