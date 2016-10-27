from flask import json
from nwpc_monitor_web.app import app, redis_client, mongodb_client

nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status

owner_list = {
    'nwp_xp':{
        'repos':[
            {'id': 1, 'name': 'nwpc_op'},
            {'id': 2, 'name': 'nwpc_qu'},
            {'id': 3, 'name': 'eps_nwpc_qu'},
            {'id': 4, 'name': 'nwpc_pd'},
            {'id': 5, 'name': 'draw_ncl'}
        ]
    },
    'nwp_pos':{
        'repos':[
            {'id':1, 'name': 'nwpc_sp'},
        ]
    },
    'nwp_vfy':{
        'repos':[
            {'id':1, 'name': 'nwpc_vfy'}
        ]
    },
    'wangdp':{
        'repos':[
            {'id':1, 'name': 'nwpc_wangdp'}
        ]
    }
}


def get_owner_repo_status(owner, repo):
    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
    message_string = redis_client.get(key)
    if message_string is None:
        return None
    else:
        message_string = message_string.decode()
    return json.loads(message_string)