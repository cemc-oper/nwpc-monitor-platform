# NWPC Monitor Platform

A monitor platform for operation systems in NWPC.

## Docker

### Build images

```bash
docker build --rm -t nwpc/nmp-base -f ./docker/base/Dockerfile .
docker build --rm -t nwpc/nmp-broker -f ./docker/broker/Dockerfile .
docker build --rm -t nwpc/nmp-scheduler -f ./docker/task_scheduler/Dockerfile .
```


### Use container

broker


```bash
docker run -d -p 6201:80 \
    -v /some/config/file/path:/etc/nwpc-monitor-platform/nwpc-monitor-broker/config.yaml \
    nwpc/nmp-broker
```

task scheduler

```bash
docker run -d \
    -v /some/config/task_scheduler:/etc/nwpc-monitor-platform/nwpc-monitor-task-scheduler
    nwpc/nmp-scheduler worker

docker run -d \
    -v /some/config/task_scheduler:/etc/nwpc-monitor-platform/nwpc-monitor-task-scheduler
    nwpc/nmp-scheduler beat
```

## LICENSE

Copyright &copy; 2015-2018, Perilla Roc.

`nwpc-monitor-platfrorm` is licensed under [GPL v3.0](LICENSE.md)