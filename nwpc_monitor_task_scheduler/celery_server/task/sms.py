#!/usr/bin/env python3
# coding=utf-8
import json
from fabric.api import run, cd, execute, env
from celery import group

from nwpc_monitor_task_scheduler.celery_server.celery import app, task_config


"""
SMS Status
"""


@app.task()
def get_sms_status_task(repo):

    owner_name = repo['owner']
    repo_name = repo['repo']
    sms_user = repo['sms_user']
    sms_name = repo['sms_name']

    config_dict = task_config.config
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

    def get_sms_status(sms_user, sms_name, user):
        with cd(project_dir):
            run("{program} {script} -o {owner} -r {repo} -u {user} -n {sms_name}".format(
                program=project_program,
                script=project_script,
                owner=owner_name,
                repo=repo_name,
                sms_user=sms_user,
                sms_name=sms_name,
                user=user
            ))

    execute(get_sms_status, sms_user=sms_user, sms_name=sms_name, user=user)


@app.task()
def get_group_sms_status_task():
    config_dict = task_config.config

    repos = config_dict['group_sms_status_task']

    # celery task group
    g = group(get_sms_status_task.s(a_repo) for a_repo in repos)
    result = g.delay()
    return


@app.task()
def get_sms_node_task(args):
    config_dict = task_config.config
    project_dir = config_dict['sms_node_task']['project']['dir']
    project_program = config_dict['sms_node_task']['project']['program']
    project_script = config_dict['sms_node_task']['project']['script']

    host = args['auth']['host']
    port = args['auth']['port']
    user = args['auth']['user']
    password = args['auth']['password']

    env_hosts = ['{user}@{host}'.format(user=user, host=host)]
    env_password = '{password}'.format(password=password)

    env.hosts = env_hosts
    env.password = env_password

    def check_sms_variable(sms_info, variable_task):
        sms_server = sms_info['sms_server']
        sms_user = sms_info['sms_user']
        sms_password = sms_info['sms_password']

        node_path = variable_task['node_path']
        var_name = variable_task['name']
        var_type = variable_task['type']
        var_value = variable_task['value']

        with cd(project_dir):
            result = run(
                "{program} {script} --sms-server={sms_server} "
                "--sms-user={sms_user} --sms-password {sms_password} --node-path={node_path}"
                .format(
                    program=project_program,
                    script=project_script,
                    sms_server=sms_server,
                    sms_user=sms_user,
                    sms_password=sms_password,
                    node_path=node_path
                ))
            response_json_string = '\n'.join(result.splitlines()[1:])
            sms_node_dict = json.loads(response_json_string)
            sms_node = SmsNode.

            var = sms_node.get_variable()


    current_task = args['task']
    variables = current_task['variables']

    for a_variable in variables:
        execute(check_sms_variable, sms_info=args['sms'], variable_task=a_variable)


if __name__ == "__main__":
    args = {
        'auth': {
            'host': 'uranus.hpc.nmic.cn',
            'port': '22',
            'user': 'wangdp',
            'password': '***REMOVED***'
        },
        'sms': {
            'sms_server': 'nwpc_wangdp',
            'sms_user': 'wangdp',
            'sms_password': '1',
            'sms_node': '/windroc_info'
        },
        'task': {
            'type': 'sms-task',
            'trigger': [
                {
                    'type': 'time',
                    'time': '11:35:00'
                }
            ],
            'variables': [
                {
                    'node_path': '/grapes_meso_post/00/chartos',
                    'name': 'SMSDATE',
                    'type': 'date',
                    'value': 'current'
                }
            ]
        }
    }
    get_sms_node_task(args)