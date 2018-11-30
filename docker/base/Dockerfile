FROM python:3

LABEL maintainer="perillaroc@gmail.com"

RUN pip3 install pyyaml requests \
    redis pymongo  sqlalchemy mongoengine mysql-connector-python \
    click flask flask-sqlalchemy \
    grpcio googleapis-common-protos

COPY vendor/ /srv/nmp/vendor/
COPY nmp-model/ /srv/nmp/nmp-model/

RUN cd /srv/nmp/vendor/nwpc-hpc-model; pip install . \
    && cd /srv/nmp/vendor/nwpc-workflow-model; pip install . \
    && cd /srv/nmp/nmp-model; pip install . \
    && cd /srv/nmp \
    && rm -rf vendor nmp-model

WORKDIR /srv/nmp

CMD ["bash"]