#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import
import os
import yaml
from celery.schedules import crontab

# load settings from config file.
config_file_name = "celery_server.config.yaml"
if 'NWPC_MONITOR_PLATFORM_CONF_DIR' in os.environ:
    config_file_directory = os.environ['NWPC_MONITOR_PLATFORM_CONF_DIR']
elif 'NWPC_MONITOR_PLATFORM_BASE' in os.environ:
    config_file_directory = os.environ['NWPC_MONITOR_PLATFORM_BASE'] + "/conf"
else:
    config_file_directory = os.path.dirname(__file__) + "/../conf"
config_file_path = config_file_directory + "/" + config_file_name
print "config file path:", config_file_path

with open(config_file_path, 'r') as config_file:
    config_dict = yaml.load(config_file)

    rabbitmq_host = config_dict['celery_server']['rabbitmq']['host']
    rabbitmq_port = config_dict['celery_server']['rabbitmq']['port']
    mysql_host = config_dict['celery_server']['mysql']['host']

task_scheduler_celery_broker = 'amqp://guest:guest@{host}:{port}//'.format(host=rabbitmq_host, port=rabbitmq_port)
task_scheduler_celery_backend = 'db+mysql://windroc:shenyang@{host}/celery_backend'.format(host=mysql_host)

###################
# celery config
###################

# broker
BROKER_URL = '{task_scheduler_celery_broker}'.format(
    task_scheduler_celery_broker=task_scheduler_celery_broker)

# backend
CELERY_RESULT_BACKEND = '{task_scheduler_celery_backend}'.format(
    task_scheduler_celery_backend=task_scheduler_celery_backend)

CELERY_INCLUDE = ['nwpc_monitor_task_scheduler.celery_server.tasks']

# celery beat
CELERYBEAT_SCHEDULE = {
    'collect_sms_suite_status': {
        'task': 'nwpc_monitor_task_scheduler.celery_server.tasks.get_group_sms_status_task',
        'schedule': crontab(minute='*/1')
    },
    'update_dingtalk_access_token': {
        'task': 'nwpc_monitor_task_scheduler.celery_server.tasks.update_dingtalk_token_task',
        'schedule': crontab(minute='*/30')
    }
}