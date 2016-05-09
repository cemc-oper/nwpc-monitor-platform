from __future__ import absolute_import
from celery import Celery

app = Celery('nwpc_monitor_platform_pipeline')

app.config_from_object('nwpc_monitor_task_scheduler.celery_config')


if __name__ == '__main__':
    app.start()
