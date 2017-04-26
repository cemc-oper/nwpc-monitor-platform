#!/usr/bin/env python3
# coding=utf-8
import datetime
import json
import gzip
import requests
from fabric.api import run, cd, execute, env
from celery import group

from nwpc_monitor_task_scheduler.celery_server.celery import app
from nwpc_work_flow_model.sms.sms_node import SmsNode


"""
SMS Status
"""


@app.task()
def get_sms_status_task(repo):

    owner_name = repo['owner']
    repo_name = repo['repo']
    sms_user = repo['sms_user']
    sms_name = repo['sms_name']

    config_dict = app.task_config.config
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
    config_dict = app.task_config.config

    repos = config_dict['group_sms_status_task']

    # celery task group
    g = group(get_sms_status_task.s(a_repo) for a_repo in repos)
    result = g.delay()
    return


def check_sms_node(project_conf, sms_info, sms_node):

    project_dir = project_conf['dir']
    project_program = project_conf['program']
    project_script = project_conf['script']

    sms_server = sms_info['sms_server']
    sms_user = sms_info['sms_user']
    sms_password = sms_info['sms_password']

    node_path = sms_node['node_path']
    check_type = sms_node['type']
    if check_type == 'variable':
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
                check_result = {
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
                    check_result['is_condition_fit'] = is_condition_fit
                else:
                    print("current var type is not supported", var_type)

                variables_result.append(check_result)

        return {
            'node_path': node_path,
            "type": "variable",
            'variables': variables_result
        }

    elif check_type == 'status':
        value_object = sms_node['value']

        check_result = None

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

            status = sms_node.status[:3]

            is_condition_fit = None
            if value_object['operator'] == 'in':
                fields = value_object['fields']
                if status in fields:
                    is_condition_fit = True
                else:
                    is_condition_fit = False
            check_result = {
                'expected_value': value_object,
                'value': status,
                'is_condition_fit': is_condition_fit
            }

        return {
            'node_path': node_path,
            "type": check_type,  # status
            'check_result': check_result
        }
    else:
        return {
            'node_path': node_path,
            'type': check_type,  # status
            'error': 'check_type_not_supported'
        }


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
            'type': 'sms-node',
            'trigger': [
                {
                    'type': 'time',
                    'time': '11:35:00'
                }
            ],
            "nodes": [
                {
                    'node_path': '/grapes_meso_post',
                    'type': 'variable',
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
    config_dict = app.task_config.config

    host = args['auth']['host']
    port = args['auth']['port']
    user = args['auth']['user']
    password = args['auth']['password']

    env_hosts = ['{user}@{host}'.format(user=user, host=host)]
    env_password = '{password}'.format(password=password)

    env.hosts = env_hosts
    env.password = env_password

    current_task = args['task']
    nodes = current_task['nodes']

    node_result = []
    for a_node in nodes:
        result = execute(
            check_sms_node,
            project_conf=config_dict['sms_node_task']['project'],
            sms_info=args['sms'],
            sms_node=a_node)
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
            'type': 'sms-node',
            'trigger': [
                {
                    'type': 'time',
                    'time': '11:35:00'
                }
            ],
            "nodes": [
                {
                    'node_path': '/grapes_meso_post',
                    'type': 'variable',
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
