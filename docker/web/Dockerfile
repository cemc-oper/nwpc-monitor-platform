FROM nwpcc/nmp-base

LABEL maintainer="perillaroc@gmail.com"

COPY nmp-web/ /srv/nmp-web/

RUN cd /srv/nmp-web \
    && pip install .

WORKDIR /srv/nmp-web

EXPOSE 80

ENTRYPOINT ["python3", "./run_website.py"]

CMD ["--config-file=/etc/nmp-web/config.yaml"]