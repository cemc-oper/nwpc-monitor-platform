FROM node:latest as broker_web_builder

RUN mkdir -p /srv/nwpc-monitor-platform

COPY nmp-broker/static/ /srv/static/

RUN cd /srv/static \
    && yarn install \
    && npm run build

FROM nwpc/nmp-base

LABEL maintainer="perillaroc@gmail.com"

# RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

ENV NWPC_MONITOR_PLATFORM_BASE /srv/nwpc-monitor-platform
ENV NWPC_MONITOR_BROKER_CONFIG /etc/nmp-broker/config.yaml

COPY nmp-broker ${NWPC_MONITOR_PLATFORM_BASE}/nmp-broker/
COPY --from=broker_web_builder /srv/static ${NWPC_MONITOR_PLATFORM_BASE}/nmp-broker/static/

RUN cd ${NWPC_MONITOR_PLATFORM_BASE}/nmp-broker \
    && pip install .

WORKDIR $NWPC_MONITOR_PLATFORM_BASE

EXPOSE 80

ENTRYPOINT ["python3", "./nmp-broker/run_broker_server.py", "-c /etc/nmp-broker/config.yaml"]
