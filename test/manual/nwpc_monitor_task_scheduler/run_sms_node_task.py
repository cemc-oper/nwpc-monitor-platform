#!/usr/bin/env python3
import os
import sys
import json
import yaml

sys.path.append(os.path.dirname(__file__)+"/../../../")
from nwpc_monitor_task_scheduler.celery_server.task import sms


def run_single_task():
    args = {
        'owner': 'wangdp',
        'repo': 'nwpc_wangdp',
        'auth': {
            'host': 'uranus-bk.hpc.nmic.cn',
            'port': '22',
            'user': 'nwp',
            'password': 'nwpop'
        },
        'sms': {
            'sms_server': 'eps_nwpc_qu',
            'sms_user': 'nwp_qu',
            'sms_password': '1'
        },
        'task': {
            'name': 'geps_t639_06',
            'type': 'sms-task',
            'trigger': [
                {
                    'type': 'time',
                    'time': '11:35:00'
                }
            ],
            "nodes": [
                {
                    'node_path': '/geps_t639/06/control/obs/sst_make',
                    'type': 'status',
                    'value': {
                        'operator': 'in',
                        'fields': [
                            'sub',
                            'act',
                            'com'
                        ]
                    }
                }
            ]
        }
    }
    print(json.dumps(sms.get_sms_node_task(args), indent=2))


def run_variable_task():
    args = {
        'owner': 'wangdp',
        'repo': 'nwpc_wangdp',
        'auth': {
            'host': 'uranus-bk.hpc.nmic.cn',
            'port': '22',
            'user': 'nwp',
            'password': 'nwpop'
        },
        'sms': {
            'sms_server': 'eps_nwpc_qu',
            'sms_user': 'nwp_qu',
            'sms_password': '1'
        },
        'task': {
            'name': 'geps_t639',
            'type': 'sms-node',
            'trigger': [
                {
                    'type': 'time',
                    'time': '11:35:00'
                }
            ],
            "nodes": [
                {
                    'node_path': '/geps_t639',
                    'type': 'variable',
                    'name': 'SMSDATE',
                    'value': {
                        'type': 'date',
                        'value': '20170425'
                    }
                }
            ]
        }
    }
    print(json.dumps(sms.get_sms_node_task(args), indent=2))


def run_task_in_config_file():
    config_file_path = "/vagrant/test/manual/nwpc_monitor_task_scheduler/data/nwpc_pd.config.yaml"
    with open(config_file_path, 'r') as config_file:
        config_dict = yaml.load(config_file)
        config = config_dict

    if config is None:
        print("Error in loading config")
        return

    task_list = config['task_list']
    for a_task in task_list:
        args = {
            'owner': config['owner'],
            'repo': config['repo'],
            'auth': config['auth'],
            'sms': config['sms'],
            'task': a_task
        }
        print(json.dumps(sms.get_sms_node_task(args), indent=2))

if __name__ == "__main__":
    run_task_in_config_file()
    # run_single_task()
    # run_variable_task()
