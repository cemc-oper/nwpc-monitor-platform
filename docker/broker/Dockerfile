FROM node:latest as broker_web_builder

COPY nmp-broker/static/ /srv/static/

RUN cd /srv/static \
    && yarn install \
    && npm run build

FROM nwpcc/nmp-base

LABEL maintainer="perillaroc@gmail.com"

ENV NWPC_MONITOR_BROKER_CONFIG /etc/nmp-broker/config.yaml

COPY nmp-broker/ /srv/nmp-broker/
COPY --from=broker_web_builder /srv/static/dist/ /srv/nmp-broker/static/dist/

RUN cd /srv/nmp-broker \
    && pip install .

WORKDIR /srv/nmp-broker

EXPOSE 80

ENTRYPOINT ["python3", "./nmp-broker/run_broker_server.py"]

CMD ["-c /etc/nmp-broker/config.yaml"]