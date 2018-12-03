# NWPC Monitor Platform

A monitor platform for operation systems in NWPC.

## Docker

### Build images

```bash
docker build --rm -t nwpcc/nmp-base -f ./docker/base/Dockerfile .
docker build --rm -t nwpcc/nmp-broker -f ./docker/broker/Dockerfile .
docker build --rm -t nwpcc/nmp-scheduler -f ./docker/task_scheduler/Dockerfile .
```


### Use container

broker


```bash
docker run -d -p 6201:80 \
    -v /some/config/file/path:/etc/nmp-broker/config.yaml \
    nwpcc/nmp-broker
```

task scheduler

```bash
docker run -d \
    -v /some/config/scheduler:/etc/nmp-scheduler nwpcc/nmp-scheduler \
    --config-file=/etc/nmp-scheduler/celery.config.yaml worker \
    --queues=nmp_sms --name=sms

docker run -d \
    -v /some/config/scheduler:/etc/nwp-scheduler nwpcc/nmp-scheduler \
    --config-file=/etc/nmp-scheduler/celery.config.yaml beat

```

## LICENSE

Copyright &copy; 2015-2018, Perilla Roc.

`nwpc-monitor-platform` is licensed under [GPL v3.0](LICENSE.md)