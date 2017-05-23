import datetime
import json
import gzip
import requests


def test_sms_node_task_api():
    node_task_result = {
        'app': 'nwpc_monitor_task_scheduler',
        'type': 'sms_node_task',
        'timestamp': datetime.datetime.now().isoformat(),
        'data': {
            'owner': 'wangdp',
            'repo': 'nwpc_wangdp',
            'request': {
                'task':  {
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
            },
            'response': {
                'nodes': [
                    {
                        'node_path': '/grapes_meso_post',
                        'check_list_result': [
                            {
                                'type': 'status',
                                'is_condition_fit': False,
                                'value': {
                                    'expected_value': {
                                        'operator': 'in',
                                        'fields': ['submitted', 'active', 'complete']
                                    },
                                    'value': 'queue'
                                }
                            },
                            {
                                'type': 'variable',
                                'name': 'SMSDATE',
                                'is_condition_fit': True,
                                'value': {
                                    'expected_value': '20170523',
                                    'value': '20170523'
                                }
                            },

                        ]
                    }
                ]
            }
        }
    }

    post_data = {
        'message': json.dumps(node_task_result)
    }

    gzipped_data = gzip.compress(bytes(json.dumps(post_data), 'utf-8'))
    url = 'http://10.28.32.175:6221/api/v2/hpc/sms/{owner}/{repo}/node-task'.format(
        owner='wangdp',
        repo='nwpc_wangdp'
    )
    requests.post(url, data=gzipped_data, headers={
        'content-encoding': 'gzip'
    })

if __name__ == "__main__":
    test_sms_node_task_api()
