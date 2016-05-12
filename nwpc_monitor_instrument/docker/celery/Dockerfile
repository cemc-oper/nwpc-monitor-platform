FROM ***REMOVED***roc/python

MAINTAINER Perilla Roc <***REMOVED***roc@gmail.com>

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

RUN yum install -y mysql-devel && pip install celery pyyaml fabric requests sqlalchemy mysql-python

VOLUME ["/src"]

ENV WORK_DIR /src
ENV APP nwpc_monitor_task_scheduler.celery_server
ENV PYTHONPATH /src

WORKDIR $WORK_DIR

USER user
CMD celery worker --workdir=${WORK_DIR} --app=${APP} -l info