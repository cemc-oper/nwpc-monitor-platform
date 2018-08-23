FROM node:latest as broker_web_builder

WORKDIR /srv
RUN mkdir -p /srv/nwpc-monitor-platform

COPY nwpc-monitor-broker/ /srv/nwpc-monitor-platform/nwpc-monitor-broker/
COPY nwpc_monitor/ /srv/nwpc-monitor-platform/nwpc_monitor/
COPY vendor/ /srv/nwpc-monitor-platform/vendor/

RUN cd /srv/nwpc-monitor-platform/nwpc-monitor-broker/static \
    && npm install \
    && npm run build

FROM nwpc/nmp-base

LABEL maintainer="perillaroc@gmail.com"

# RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

RUN pip3 install pyyaml redis pymongo requests flask-sqlalchemy

ENV NWPC_MONITOR_PLATFORM_BASE /srv/nwpc-monitor-platform
ENV NWPC_MONITOR_BROKER_CONFIG /etc/nwpc-monitor-platform/nwpc-monitor-broker/config.yaml

COPY --from=broker_web_builder ${NWPC_MONITOR_PLATFORM_BASE} ${NWPC_MONITOR_PLATFORM_BASE}

WORKDIR $NWPC_MONITOR_PLATFORM_BASE

RUN cd vendor/nwpc-hpc-model; python3 setup.py install \
    && cd ../nwpc-workflow-model; python3 setup.py install

EXPOSE 80

#USER user

CMD ["python3", "./nwpc-monitor-broker/run_broker_server.py"]
