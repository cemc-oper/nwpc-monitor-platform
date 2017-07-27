#!/usr/bin/env bash

# run nwpc monitor broker server using develop mode.

base_dir=$(cd "`dirname "$0"`"/..; pwd)
export NWPC_MONITOR_PLATFORM_BASE=${base_dir}

python3 ${NWPC_MONITOR_PLATFORM_BASE}/nwpc_monitor_broker/run_broker_server.py \
    -c ${NWPC_MONITOR_PLATFORM_BASE}/dist/broker/conf/develop.config.yaml