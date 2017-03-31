#!/usr/bin/env python
# coding=utf-8
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
    host = args['auth']['host']
    port = args['auth']['port']
    user = args['auth']['user']
    password = args['auth']['password']

    sms_server = args['sms']['sms_server']
    sms_user = args['sms']['sms_user']
    sms_password = args['sms']['sms_password']
    sms_node = args['sms']['sms_node']

    config_dict = task_config.config
    project_dir = config_dict['sms_node_task']['project']['dir']
    project_program = config_dict['sms_node_task']['project']['program']
    project_script = config_dict['sms_node_task']['project']['script']

    env_hosts = ['{user}@{host}'.format(user=user, host=host)]
    env_password = '{password}'.format(password=password)

    env.hosts = env_hosts
    env.password = env_password

    def get_sms_node(sms_server, sms_user, sms_password, sms_node):
        with cd(project_dir):
            result = run(
                "{program} {script} --sms-server={sms_server} "
                "--sms-user={sms_user} --sms-password {sms_password} --node-path={sms_node}"
                .format(
                    program=project_program,
                    script=project_script,
                    sms_server=sms_server,
                    sms_user=sms_user,
                    sms_password=sms_password,
                    sms_node=sms_node
                ))
            response_json_string = '\n'.join(result.splitlines()[1:])
            print(response_json_string)

    execute(get_sms_node, sms_server=sms_server, sms_user=sms_user, sms_password=sms_password, sms_node=sms_node)


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
        }
    }
    get_sms_node_task(args)