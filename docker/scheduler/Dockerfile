FROM nwpcc/nmp-base

LABEL maintainer="perillaroc@gmail.com"

RUN pip3 install celery fabric

COPY nmp-scheduler/ /srv/nmp-scheduler/

RUN cd /srv/nmp-scheduler \
    && pip install .

WORKDIR /srv/nmp-scheduler

ENV NWPC_MONITOR_TASK_SCHEDULER_CONFIG /etc/nmp-scheduler/celery.config.yaml

ENTRYPOINT ["python3", "nmp_scheduler/run.py"]

CMD ["--help"]
