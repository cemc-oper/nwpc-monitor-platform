#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import
from celery import Celery
from nwpc_monitor_task_scheduler.celery_server.config import CeleryConfig, TaskConfig

celery_config = CeleryConfig.load_celery_config()

app = Celery(celery_config.celery_server_config['name'])

app.config_from_object(celery_config)

task_config = TaskConfig.load_celery_config()


if __name__ == '__main__':
    app.start()
