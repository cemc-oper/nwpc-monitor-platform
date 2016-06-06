FROM ***REMOVED***roc/python:3

MAINTAINER Perilla Roc <***REMOVED***roc@gmail.com>

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

RUN yum install -y mysql-devel &&

RUN wget http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.0.4.zip#md5=3df394d89300db95163f17c843ef49df \
    && sudo yum install -y unzip \
    && unzip mysql-connector-python-2.0.4.zip \
    && cd mysql-connector-python-2.0.4 \
    && python3 setup.py build \
    && sudo /usr/local/bin/python3 setup.py install

RUN pip3 install celery pyyaml fabric requests sqlalchemy

VOLUME ["/src"]

ENV WORK_DIR /src
ENV APP nwpc_monitor_task_scheduler.celery_server
ENV PYTHONPATH /src

WORKDIR $WORK_DIR

USER user
CMD celery worker --workdir=${WORK_DIR} --app=${APP} -l info