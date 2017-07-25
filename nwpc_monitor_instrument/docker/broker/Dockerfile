FROM node:latest as broker_web_builder

WORKDIR /srv

RUN git clone https://github.com/perillaroc/nwpc-monitor-platform.git \
    && cd ./nwpc-monitor-platform/nwpc_monitor_broker/static \
    && npm install \
    && npm run build

FROM perillaroc/flask

LABEL maintainer="perillaroc@gmail.com"

# RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

RUN pip3 install pyyaml redis pymongo requests flask-sqlalchemy

RUN wget https://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.1.6.tar.gz \
    && tar zxvf mysql-connector-python-2.1.6.tar.gz \
    && cd mysql-connector-python-2.1.6 \
    && python3 setup.py build \
    && python3 setup.py install

ENV NWPC_MONITOR_PLATFORM_BASE /srv/nwpc-monitor-platform
ENV NWPC_MONITOR_BROKER_CONFIG /etc/nwpc-monitor-platform/nwpc-monitor-broker/config.yaml

COPY --from=broker_web_builder ${NWPC_MONITOR_PLATFORM_BASE} ${NWPC_MONITOR_PLATFORM_BASE}

WORKDIR $NWPC_MONITOR_PLATFORM_BASE

RUN cd vendor/nwpc-hpc-model; python3 setup.py install \
    && cd ../nwpc-work-flow-model; python3 setup.py install

EXPOSE 80

#USER user

CMD ["python3", "./nwpc_monitor_broker/run_broker_server.py"]
