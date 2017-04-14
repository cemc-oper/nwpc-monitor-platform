#!/usr/bin/env python
# coding=utf-8
import yaml
import datetime

from celery import Celery
from celery.schedules import crontab
from nwpc_monitor_task_scheduler.celery_server.config import CeleryConfig, TaskConfig


celery_config = CeleryConfig.load_celery_config()

app = Celery(celery_config.celery_server_config['name'])

app.config_from_object(celery_config)

task_config = TaskConfig.load_celery_config()


from nwpc_monitor_task_scheduler.celery_server.task.sms import get_sms_node_task


@app.on_after_configure.connect
def setup_sms_node_periodic_task(sender, **kwargs):
    config_file_path = "/vagrant/nwpc_monitor_task_scheduler/conf/sms_node_task/nwpc_op.config.yaml"
    with open(config_file_path, 'r') as config_file:
        config_dict = yaml.load(config_file)
        config = config_dict

    if config is None:
        print("Error in loading config")
        return

    task_list = config['task_list']
    for a_task in task_list:
        task_triggers = a_task['trigger']
        task_args = {
            'owner': config['owner'],
            'repo': config['repo'],
            'auth': config['auth'],
            'sms': config['sms'],
            'task': a_task
        }
        for a_trigger in task_triggers:
            trigger_type = a_trigger['type']
            if trigger_type == 'time':
                trigger_time = datetime.datetime.strptime(a_trigger['time'],"%H:%M:%S")
                crontab_param_dict = {
                    'minute': trigger_time.minute,
                    'hour': trigger_time.hour
                }
                print('add periodic_task', a_task)
                # sender.add_periodic_task(
                #     crontab(**crontab_param_dict),
                #     get_sms_node_task.s(task_args)
                # )
                sender.add_periodic_task(
                    1,
                    get_sms_node_task.s(task_args),
                    name=a_task['name']
                )
            else:
                print("trigger type is not supported:", trigger_type)

if __name__ == '__main__':
    app.start()
