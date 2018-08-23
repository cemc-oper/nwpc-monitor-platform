FROM python:3

LABEL maintainer="perillaroc@gmail.com"

RUN pip3 install flask

ENV WORK_DIR /srv

WORKDIR $WORK_DIR

RUN wget https://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.1.6.tar.gz \
    && tar zxvf mysql-connector-python-2.1.6.tar.gz \
    && cd mysql-connector-python-2.1.6 \
    && python3 setup.py build \
    && python3 setup.py install \
    && rm -rf mysql-connector-python-2.1.6

EXPOSE 80

CMD ["bash"]