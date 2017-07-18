FROM node:latest as broker_web_builder
RUN cd /srv \
    && git clone https://github.com/***REMOVED***roc/nwpc-monitor-platform.git \
    && cd /srv/nwpc-monitor-platform/nwpc_monitor_broker/static \
    && npm install \
    && npm run build

FROM ***REMOVED***roc/flask

MAINTAINER Perilla Roc <***REMOVED***roc@gmail.com>

#RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

RUN pip3 install pyyaml redis pymongo requests flask-sqlalchemy

RUN apt-get update \
    && apt-get install unzip \
    && rm -rf /var/lib/apt/lists/*

RUN wget http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.0.5.zip \
    && unzip mysql-connector-python-2.0.5.zip \
    && cd mysql-connector-python-2.0.5 \
    && python3 setup.py build \
    && python3 setup.py install

COPY --from=broker_web_builder /srv/nwpc-monitor-platform /srv/nwpc-monitor-platform

RUN cd /srv/nwpc-monitor-platform/vendor/nwpc-hpc-model; python3 setup.py install \
    && cd /srv/nwpc-monitor-platform/vendor/nwpc-work-flow-model; python3 setup.py install

ENV WORK_DIR /srv/nwpc-monitor-platform
ENV NWPC_MONITOR_PLATFORM_BASE $WORK_DIR
ENV NWPC_MONITOR_BROKER_CONFIG /etc/nwpc-monitor-platform/nwpc-monitor-broker/config.yaml
WORKDIR $WORK_DIR

EXPOSE 80

#USER user

CMD ["python3", "/srv/nwpc-monitor-platform/nwpc_monitor_broker/run_broker_server.py"]
