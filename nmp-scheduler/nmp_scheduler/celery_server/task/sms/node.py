import datetime
import gzip
import json

import requests
from fabric import Connection
import grpc

from nmp_scheduler.celery_server.celery import app
from nwpc_workflow_model.sms import SmsNode


def check_sms_node(collector_config, owner, repo, sms_info, sms_node):
    """
    check a sms node. return check result.

    :param collector_config: collector_config
    :param owner: owner name
    :param repo: repo name
    :param sms_info: sms server information
        {
            'sms_host': sms host,
            'sms_prog': sms RPC prog,
            'sms_name': sms server name,
            'sms_user': sms user,
            'sms_password': sms password
        }
    :param sms_node: sms node task for one node path
        {
            'node path': node path,
            'check_list': check list,
        }

        an item in check list:
        common fields:
        {
           'type': check type, [ variable, status ]
        }
        check type related fields:
        * variable, check variable value, there may be more than one variable for a single node path.
            {
                'name': variable name,
                'value': {
                    'type': variable type,
                    'operator': 'equal',
                    'fields': fields of operators, array or an object
                }
            }

        * status, check sms node status
            {
                'value': {
                    'operator': operator, such as in
                    'fields': array, []
                }
            }
    :return: check result
        {

        }
    """
    sms_host = sms_info['sms_host']
    sms_prog = sms_info['sms_prog']
    sms_name = sms_info['sms_name']
    sms_user = sms_info['sms_user']
    sms_password = sms_info['sms_password']

    node_path = sms_node['node_path']

    rpc_target = collector_config['server']['rpc_target']

    check_list_result = []

    from nmp_scheduler.celery_server.task.sms.proto import sms_collector_pb2_grpc, sms_collector_pb2
    status_request = sms_collector_pb2.VariableRequest(
        owner=owner,
        repo=repo,
        sms_host=sms_host,
        sms_prog=str(sms_prog),
        sms_name=sms_name,
        sms_user=sms_user,
        sms_password=sms_password,
        node_path=node_path,
        verbose=False
    )

    app.log.get_default_logger().info('Getting sms variable for {owner}/{repo}...'.format(
        owner=owner, repo=repo
    ))
    with grpc.insecure_channel(rpc_target) as channel:
        stub = sms_collector_pb2_grpc.SmsCollectorStub(channel)
        response = stub.CollectVariable(status_request)
        app.log.get_default_logger().info(
            'Getting sms variable for {owner}/{repo}...done: {response}'.format(
                owner=owner, repo=repo, response=response.status
            ))

    result_string = response.result
    result = json.loads(result_string)

    sms_node_dict = result['data']['response']['node']
    node_object = SmsNode.create_from_dict(sms_node_dict)

    for a_check_item in sms_node['check_list']:
        check_type = a_check_item['type']
        is_condition_fit = None
        check_result = {
            'type': check_type,
            'is_condition_fit': is_condition_fit
        }

        if check_type == 'variable':
            var_name = a_check_item['name']
            check_result['name'] = var_name

            value_type = a_check_item['value']['type']
            value_operator = a_check_item['value']['operator']

            if value_type == "date":
                if value_operator == 'equal':
                    expected_var_value = a_check_item['value']['fields']
                    if expected_var_value == 'current' or expected_var_value == 'today':
                        expected_var_value = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d")
                    elif expected_var_value == 'yesterday':
                        expected_var_value = (
                                datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1)
                        ).strftime("%Y%m%d")

                    var = node_object.get_variable(var_name)
                    if var.value == expected_var_value:
                        is_condition_fit = True
                    else:
                        is_condition_fit = False

                    check_result['value'] = var.value
                    check_result['expected_value'] = expected_var_value
                    check_result['is_condition_fit'] = is_condition_fit

        elif check_type == 'status':
            status = node_object.status
            if a_check_item['value']['operator'] == 'in':
                fields = a_check_item['value']['fields']
                if status in fields:
                    is_condition_fit = True
                else:
                    is_condition_fit = False

            check_result['value'] = status
            check_result['expected_value'] = a_check_item['value']
            check_result['is_condition_fit'] = is_condition_fit

        if is_condition_fit is None:
            print("current var check is not supported", a_check_item)

        check_list_result.append(check_result)

    return {
        'node_path': node_path,
        'check_list_result': check_list_result
    }


@app.task()
def check_sms_node_task(args):
    """

    :param args:
    {
        'owner': 'owner',
        'repo': 'repo',
        'auth': {
            'host': 'host',
            'port': 'port',
            'user': 'user',
            'password': 'password'
        },
        'sms': {
            'sms_server': 'sms_server',
            'sms_user': 'sms_user',
            'sms_password': 'sms_password'
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
                    'check_list': [
                        {
                            'type': 'variable',
                            'name': 'SMSDATE',
                            'value': {
                                'type': 'date',
                                'operator': 'equal',
                                'fields': 'current'
                            }
                        },
                        {
                            'type': 'status',
                            'value': {
                                'operator': 'in',
                                'fields': [
                                    "submitted",
                                    "active",
                                    "complete"
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    }
    :return:
    {
        'app': 'nmp_scheduler',
        'type': 'sms_node_task',
        'timestamp': iso format,
        'data': {
            'owner': owner,
            'repo': repo,
            'request': {
                'task': task object,
            },
            'response': {
                'nodes':[
                    {
                        'node_path': node_path,
                        'check_list_result': array, see check_sms_node
                    },
                    ...
                ]
            }
        }
    }

    nodes: an array of node result

    """
    config_dict = app.task_config.config

    owner = args['owner']
    repo = args['repo']

    current_task = args['task']
    nodes = current_task['nodes']

    collector_config = config_dict['sms']['node_task']['collector']

    node_result = []
    for a_node in nodes:
        result = check_sms_node(
            collector_config,
            owner=owner,
            repo=repo,
            sms_info=args['sms'],
            sms_node=a_node)
        node_result.append(result)

    result = {
        'app': 'nmp_scheduler',
        'type': 'sms_node_task',
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'data': {
            'owner': args['owner'],
            'repo': args['repo'],
            'time': datetime.datetime.utcnow().isoformat(),
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
    url = collector_config['post']['url'].format(
        owner=args['owner'],
        repo=args['repo']
    )
    requests.post(url, data=gzipped_data, headers={
        'content-encoding': 'gzip'
    })

    return result


if __name__ == "__main__":
    args = {
        'owner': 'owner',
        'repo': 'repo',
        'sms': {
            'sms_server': 'sms_server',
            'sms_user': 'sms_user',
            'sms_password': 'sms_password'
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
                    'check_list': [
                        {
                            'type': 'variable',
                            'name': 'SMSDATE',
                            'value': {
                                'type': 'date',
                                'operator': 'equal',
                                'fields': 'current'
                            }
                        },
                        {
                            'type': 'status',
                            'value': {
                                'operator': 'in',
                                'fields': [
                                    "submitted",
                                    "active",
                                    "complete"
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    }
    print(json.dumps(check_sms_node_task(args), indent=2))
