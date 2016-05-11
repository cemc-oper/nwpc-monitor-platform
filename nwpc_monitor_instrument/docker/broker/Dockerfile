FROM ***REMOVED***roc/flask

MAINTAINER Perilla Roc <***REMOVED***roc@gmail.com>

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

RUN pip install pyyaml redis requests

VOLUME ["/src"]

ENV WORK_DIR /src
ENV PYTHONPATH /src
WORKDIR $WORK_DIR

EXPOSE 5201

USER user
CMD python ${WORK_DIR}/nwpc_monitor_broker/run_broker_server.py