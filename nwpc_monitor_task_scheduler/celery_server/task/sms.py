#!/usr/bin/env python3
# coding=utf-8
import datetime
import json
import gzip
import os
import requests
import yaml
from fabric.api import run, cd, execute, env
from celery import group
from celery.schedules import crontab

from nwpc_monitor_task_scheduler.celery_server.celery import app, task_config
from nwpc_work_flow_model.sms.sms_node import SmsNode
from nwpc_monitor_task_scheduler.celery_server.config import TaskConfig


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
    """
    
    :param args: 
    {
        'owner': 'wangdp',
        'repo': 'nwpc_wangdp',
        'auth': {
            'host': 'uranus.hpc.nmic.cn',
            'port': '22',
            'user': 'wangdp',
            'password': '***REMOVED***'
        },
        'sms': {
            'sms_server': 'nwpc_wangdp',
            'sms_user': 'wangdp',
            'sms_password': '1'
        },
        'task': {
            'name': 'grapes_meso_post',
            'type': 'sms-task',
            'trigger': [
                {
                    'type': 'time',
                    'time': '11:35:00'
                }
            ],
            "nodes": [
                {
                    'node_path': '/grapes_meso_post',
                    'variables': [
                        {
                            'name': 'SMSDATE',
                            'type': 'date',
                            'value': 'current'
                        }
                    ]
                }
            ]
        }
    }
    :return: 
    {
        'app': 'nwpc_monitor_task_scheduler',
        'type': 'sms_node_task',
        'timestamp': iso format,
        'data': {
            'owner': owner,
            'repo': repo,
            'request': {
                'task': task object,
            },
            'response': {
                'nodes': node result
            }
        }
    }
    """
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

    def check_sms_variable(sms_info, sms_node):
        sms_server = sms_info['sms_server']
        sms_user = sms_info['sms_user']
        sms_password = sms_info['sms_password']

        node_path = sms_node['node_path']
        variables = sms_node['variables']

        variables_result = []

        for variable_task in variables:
            var_name = variable_task['name']
            var_type = variable_task['type']
            expected_var_value = variable_task['value']

            with cd(project_dir):
                run_result = run(
                    "{program} {script} --sms-server={sms_server} "
                    "--sms-user={sms_user} --sms-password {sms_password} --node-path={node_path}"
                    .format(
                        program=project_program,
                        script=project_script,
                        sms_server=sms_server,
                        sms_user=sms_user,
                        sms_password=sms_password,
                        node_path=node_path
                    )).splitlines()
                cur_line_no = 0
                result_length = len(run_result)
                while cur_line_no < result_length and (not run_result[cur_line_no].startswith("{")):
                    cur_line_no += 1

                response_json_string = '\n'.join(run_result[cur_line_no:])
                sms_node_dict = json.loads(response_json_string)['data']['response']['node']
                sms_node = SmsNode.create_from_dict(sms_node_dict)

                var = sms_node.get_variable(var_name)

                is_condition_fit = None
                response_result = {
                    'name': var_name,
                    'type': var_type,
                    'expected_value': expected_var_value,
                    'value': var.value,
                    'is_condition_fit': is_condition_fit
                }

                if var_type == "date":
                    if expected_var_value == 'current':
                        expected_var_value = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d")
                    if var.value == expected_var_value:
                        is_condition_fit = True
                    else:
                        is_condition_fit = False
                    response_result['is_condition_fit'] = is_condition_fit
                else:
                    print("current var type is not supported", var_type)

                variables_result.append(response_result)

        return {
            'node_path': node_path,
            'variables': variables_result
        }

    current_task = args['task']
    nodes = current_task['nodes']

    node_result = []
    for a_node in nodes:
        result = execute(check_sms_variable, sms_info=args['sms'], sms_node=a_node)
        node_result.extend(result.values())

    result = {
        'app': 'nwpc_monitor_task_scheduler',
        'type': 'sms_node_task',
        'timestamp': datetime.datetime.now().isoformat(),
        'data': {
            'owner': args['owner'],
            'repo': args['repo'],
            'request': {
                'task': args['task'],
            },
            'response': {
                'nodes': node_result
            }
        }
    }
    post_data = {
        'message': json.dumps(result)
    }

    gzipped_data = gzip.compress(bytes(json.dumps(post_data), 'utf-8'))
    url = 'http://10.28.32.175:6201/api/v2/hpc/sms/{owner}/{repo}/node-task'.format(
        owner=args['owner'],
        repo=args['repo']
    )
    requests.post(url, data=gzipped_data, headers={
        'content-encoding': 'gzip'
    })

    return result


@app.on_after_configure.connect
def setup_sms_node_periodic_task(sender, **kwargs):
    task_config_dir = TaskConfig.get_config_file_dir()
    repo_config_dir = task_config.config['sms_node_task']['repo_config_dir']
    repo_config_dir = os.path.join(task_config_dir, repo_config_dir)

    for root, dirs, files in os.walk(repo_config_dir):
        for file_path in files:
            print(file_path)
            if not file_path.endswith('yaml'):
                continue
            config_file_path = file_path
            with open(os.path.join(repo_config_dir,config_file_path), 'r') as config_file:
                config = yaml.load(config_file)

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
                        trigger_time = datetime.datetime.strptime(a_trigger['time'], "%H:%M:%S")
                        crontab_param_dict = {
                            'minute': trigger_time.minute,
                            'hour': trigger_time.hour
                        }
                        # crontab_param_dict = {
                        #     'minute': datetime.datetime.now().minute + 1,
                        #     'hour': datetime.datetime.now().hour
                        # }
                        print('add periodic_task', crontab_param_dict)
                        sender.add_periodic_task(
                            crontab(**crontab_param_dict),
                            get_sms_node_task.s(task_args)
                        )
                    else:
                        print("trigger type is not supported:", trigger_type)


if __name__ == "__main__":
    args = {
        'owner': 'wangdp',
        'repo': 'nwpc_wangdp',
        'auth': {
            'host': 'uranus.hpc.nmic.cn',
            'port': '22',
            'user': 'wangdp',
            'password': '***REMOVED***'
        },
        'sms': {
            'sms_server': 'nwpc_wangdp',
            'sms_user': 'wangdp',
            'sms_password': '1'
        },
        'task': {
            'name': 'grapes_meso_post',
            'type': 'sms-task',
            'trigger': [
                {
                    'type': 'time',
                    'time': '11:35:00'
                }
            ],
            "nodes": [
                {
                    'node_path': '/grapes_meso_post',
                    'variables': [
                        {
                            'name': 'SMSDATE',
                            'type': 'date',
                            'value': 'current'
                        }
                    ]
                }
            ]
        }
    }
    print(json.dumps(get_sms_node_task(args), indent=2))
