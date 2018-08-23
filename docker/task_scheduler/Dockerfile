FROM nwpc/nmp-base

LABEL maintainer="perillaroc@gmail.com"

RUN pip3 install celery pyyaml fabric3 requests sqlalchemy click

ENV NWPC_MONITOR_PLATFORM_BASE /srv/nwpc-monitor-platform

COPY nwpc_monitor/ ${NWPC_MONITOR_PLATFORM_BASE}/nwpc_monitor/
COPY nwpc_monitor_task_scheduler/ ${NWPC_MONITOR_PLATFORM_BASE}/nwpc_monitor_task_scheduler/
COPY vendor/ ${NWPC_MONITOR_PLATFORM_BASE}/vendor/

WORKDIR $NWPC_MONITOR_PLATFORM_BASE

RUN cd vendor/nwpc-hpc-model; python3 setup.py install \
    && cd ../nwpc-workflow-model; python3 setup.py install

ENV PYTHONPATH $NWPC_MONITOR_PLATFORM_BASE
ENV NWPC_MONITOR_TASK_SCHEDULER_CONFIG /etc/nwpc-monitor-platform/nwpc-monitor-task-scheduler/celery.config.yaml

ENTRYPOINT ["python3", "nwpc_monitor_task_scheduler/run.py"]

CMD ["--help"]
