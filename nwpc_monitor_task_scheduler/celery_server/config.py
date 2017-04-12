#!/usr/bin/env python
# coding=utf-8
import os
import yaml
from celery.schedules import crontab


class CeleryConfig(object):
    def __init__(self, config_file_path):
        with open(config_file_path, 'r') as config_file:
            config_dict = yaml.load(config_file)
            celery_server_config = config_dict['celery_server']
            self.celery_server_config=celery_server_config
            broker_config = celery_server_config['broker']
            backend_config = celery_server_config['backend']
            beat_config = celery_server_config['beat_schedule']

            if 'rabbitmq' in broker_config:
                rabbitmq_host = broker_config['rabbitmq']['host']
                rabbitmq_port = broker_config['rabbitmq']['port']
                task_scheduler_celery_broker = 'amqp://guest:guest@{host}:{port}//'.format(
                    host=rabbitmq_host, port=rabbitmq_port
                )
                self.broker_url = '{task_scheduler_celery_broker}'.format(
                    task_scheduler_celery_broker=task_scheduler_celery_broker)

            if 'mysql' in backend_config:
                mysql_host = backend_config['mysql']['host']
                mysql_port = backend_config['mysql']['port']
                mysql_user = backend_config['mysql']['user']
                mysql_password = backend_config['mysql']['password']
                task_scheduler_celery_backend = \
                    'db+mysql+mysqlconnector://{user}:{password}@{host}:{port}/celery_backend'.format(
                        user=mysql_user, password=mysql_password,
                        host=mysql_host, port=mysql_port
                    )
                self.result_backend = '{task_scheduler_celery_backend}'.format(
                    task_scheduler_celery_backend=task_scheduler_celery_backend)

            self.include = [
                'nwpc_monitor_task_scheduler.celery_server.task'
            ]

            # celery beat
            beat_schedule = {}
            for a_beat_item in beat_config:
                item_schedule = a_beat_item['schedule']
                if item_schedule['type'] == 'crontab':
                    schedule_param = item_schedule['param']
                    crontab_param_dict = {}
                    for a_param in schedule_param:
                        crontab_param_dict[a_param] = schedule_param[a_param]
                    beat_schedule[a_beat_item['name']] = {
                        'task': a_beat_item['task'],
                        'schedule': crontab(**crontab_param_dict),
                        'args': ()
                    }
                else:
                    print('we do not support this type: {schedule_type}'.format(schedule_type=item_schedule['type']))

            print(beat_schedule)
            self.beat_schedule = beat_schedule

    @staticmethod
    def load_celery_config():
        config_file_name = "celery_server.production.config.yaml"
        if 'MODE' in os.environ:
            mode = os.environ['MODE']
            if mode == 'production':
                config_file_name = "celery_server.production.config.yaml"
            elif mode == 'develop':
                config_file_name = "celery_server.develop.config.yaml"

        config_file_directory = os.path.dirname(__file__) + "/../conf"

        config_file_path = config_file_directory + "/" + config_file_name
        print("config file path:", config_file_path)

        config = CeleryConfig(config_file_path)
        return config


class TaskConfig(object):
    def __init__(self, config_file_path):
        with open(config_file_path, 'r') as config_file:
            config_dict = yaml.load(config_file)
            self.config = config_dict

    @staticmethod
    def load_celery_config():
        config_file_name = "task.production.config.yaml"
        if 'MODE' in os.environ:
            mode = os.environ['MODE']
            if mode == 'production':
                config_file_name = "task.production.config.yaml"
            elif mode == 'develop':
                config_file_name = "task.develop.config.yaml"

        config_file_directory = os.path.dirname(__file__) + "/../conf"

        config_file_path = config_file_directory + "/" + config_file_name
        # print "task config file path:", config_file_path

        config = TaskConfig(config_file_path)
        return config
