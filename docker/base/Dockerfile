FROM python:3

LABEL maintainer="perillaroc@gmail.com"

RUN pip3 install pyyaml requests \
    redis pymongo  sqlalchemy mongoengine mysql-connector-python \
    click flask flask-sqlalchemy \
    grpcio googleapis-common-protos

ENV NWPC_MONITOR_PLATFORM_BASE /srv/nwpc-monitor-platform

COPY vendor/ ${NWPC_MONITOR_PLATFORM_BASE}/vendor/
COPY nmp-model/ ${NWPC_MONITOR_PLATFORM_BASE}/nmp-model/

RUN cd ${NWPC_MONITOR_PLATFORM_BASE}/vendor/nwpc-hpc-model; pip install . \
    && cd ${NWPC_MONITOR_PLATFORM_BASE}/vendor/nwpc-workflow-model; pip install . \
    && cd ${NWPC_MONITOR_PLATFORM_BASE}/nmp-model; pip install . \
    && cd ${NWPC_MONITOR_PLATFORM_BASE} \
    && rm -rf vendor nmp-model

ENV WORK_DIR ${NWPC_MONITOR_PLATFORM_BASE}

WORKDIR $WORK_DIR

CMD ["bash"]