from __future__ import absolute_import
from celery import Celery
from nwpc_monitor_task_scheduler.celery_server import celery_config

app = Celery('nwpc_monitor_platform_pipeline')

app.config_from_object(celery_config)


if __name__ == '__main__':
    app.start()
