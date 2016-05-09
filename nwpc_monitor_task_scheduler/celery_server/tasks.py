#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import
import os

from fabric.api import run, cd, execute, env
from celery import group
import requests
import yaml

from nwpc_monitor_task_scheduler.celery_server.celery import app

# 参数配置文件
CONFIG_FILE_NAME = 'task.config.yaml'
if 'NWPC_MONITOR_PLATFORM_CONF_DIR' in os.environ:
    CONFIG_FILE_DIR = os.environ['NWPC_MONITOR_PLATFORM_CONF_DIR']
elif 'NWPC_MONITOR_PLATFORM_BASE' in os.environ:
    CONFIG_FILE_DIR = os.environ['NWPC_MONITOR_PLATFORM_BASE'] + "/conf"
else:
    CONFIG_FILE_DIR = os.path.dirname(__file__) + "../conf"


###############
#   SMS Status
###############


@app.task()
def get_sms_status_task(repo):

    sms_user = repo['sms_user']
    sms_name = repo['sms_name']

    config_file_name = CONFIG_FILE_NAME
    config_file_path = CONFIG_FILE_DIR + "/" + config_file_name
    with open(config_file_path, 'r') as config_file:
        config_dict = yaml.load(config_file)
        hpc_user = config_dict['sms_status_task']['hpc']['user']
        hpc_password = config_dict['sms_status_task']['hpc']['password']
        hpc_host = config_dict['sms_status_task']['hpc']['host']
        project_dir = config_dict['sms_status_task']['project']['dir']
        project_program = config_dict['sms_status_task']['project']['program']
        project_script = config_dict['sms_status_task']['project']['script']

    user = repo.get('user', hpc_user)
    password = repo.get('password', hpc_password)
    host = repo.get('host', hpc_host)

    env_hosts = ['{user}@{host}'.format(user=user, host=host)]
    env_password = '{password}'.format(password=password)

    env.hosts = env_hosts
    env.password = env_password

    def read_sms_log(sms_user, sms_name, user):
        with cd(project_dir):
            run("{program} {script} -u {user} -n {sms_name}".format(
                program=project_program,
                script=project_script,
                sms_user=sms_user,
                sms_name=sms_name,
                user=user
            ))

    execute(read_sms_log, sms_user=sms_user, sms_name=sms_name, user=user)


@app.task()
def get_group_sms_status_task():
    config_file_name = CONFIG_FILE_NAME
    config_file_path = CONFIG_FILE_DIR + "/" + config_file_name

    with open(config_file_path, 'r') as config_file:
        config_dict = yaml.load(config_file)
        repos = config_dict['group_sms_status_task']

    # celery task group
    g = group(get_sms_status_task.s(a_repo) for a_repo in repos)
    result = g.delay()
    return


###############
#   Dingtalk
###############


@app.task()
def update_dingtalk_token_task():
    config_file_name = CONFIG_FILE_NAME
    config_file_path = CONFIG_FILE_DIR + "/" + config_file_name

    with open(config_file_path, 'r') as config_file:
        config_dict = yaml.load(config_file)
        url = config_dict['update_dingtalk_token_task']['url']

    requests.get(url)
    return


if __name__ == "__main__":
    # from sms_log_agent_monitor.tasks import *
    r = update_dingtalk_token_task.delay()