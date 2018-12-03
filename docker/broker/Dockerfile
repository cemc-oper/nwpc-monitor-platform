FROM node:latest as broker_web_builder

COPY nmp-broker/static/ /srv/static/

RUN cd /srv/static \
    && yarn install \
    && npm run build

FROM nwpcc/nmp-base

LABEL maintainer="perillaroc@gmail.com"

COPY nmp-broker/ /srv/nmp-broker/
COPY --from=broker_web_builder /srv/static/dist/ /srv/nmp-broker/static/dist/

RUN cd /srv/nmp-broker \
    && pip install .

WORKDIR /srv/nmp-broker

EXPOSE 80

ENTRYPOINT ["python3", "./run_broker_server.py"]

CMD ["--config-file=/etc/nmp-broker/config.yaml"]