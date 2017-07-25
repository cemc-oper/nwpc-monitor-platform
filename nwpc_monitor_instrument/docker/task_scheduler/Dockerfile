FROM python:3

LABEL maintainer="perillaroc@gmail.com"

RUN wget https://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.1.6.tar.gz \
    && tar zxvf mysql-connector-python-2.1.6.tar.gz \
    && cd mysql-connector-python-2.1.6 \
    && python3 setup.py build \
    && python3 setup.py install

RUN pip3 install celery pyyaml fabric3 requests sqlalchemy click

RUN cd /srv \
    && git clone https://github.com/perillaroc/nwpc-monitor-platform.git \
    && cd nwpc-monitor-platform/vendor/nwpc-hpc-model \
    && python3 setup.py install \
    && cd ../nwpc-work-flow-model \
    && python3 setup.py install

ENV NWPC_MONITOR_PLATFORM_BASE /srv/nwpc-monitor-platform
ENV PYTHONPATH $NWPC_MONITOR_PLATFORM_BASE
ENV NWPC_MONITOR_TASK_SCHEDULER_CONFIG /etc/nwpc-monitor-platform/nwpc-monitor-task-scheduler/celery.config.yaml
WORKDIR $NWPC_MONITOR_PLATFORM_BASE

ENTRYPOINT ["python3", "nwpc_monitor_task_scheduler/run.py"]

CMD ["--help"]
