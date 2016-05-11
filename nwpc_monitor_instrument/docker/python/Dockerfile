FROM centos:7

MAINTAINER Perilla Roc <***REMOVED***roc@gmail.com>

RUN yum install -y gcc python-devel

RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && python get-pip.py

CMD ["python2"]