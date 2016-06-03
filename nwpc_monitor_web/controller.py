# coding=utf-8
from nwpc_monitor_web import app, redis_client
from nwpc_monitor.nwpc_log.visitor import pre_order_travel_dict, SubTreeNodeVisitor

from flask import json, request, jsonify,render_template

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
    return json.loads(message_string)

@app.route('/')
def get_index_page():
    return render_template("index.html")


@app.route('/<owner>')
def get_owner_page(owner):
    repo_list = []
    if owner in owner_list:
        repo_list = owner_list[owner]['repos']

    owner_repo_status = []
    for a_repo in repo_list:
        a_repo_name = a_repo['name']
        cache_value = get_owner_repo_status(owner, a_repo_name)
        repo_status = None
        if cache_value is not None:
            bunch_dict = cache_value['status']

            repo_status = bunch_dict['status']
        owner_repo_status.append({
            'owner': owner,
            'repo': a_repo_name,
            'status': repo_status
        })

    return render_template("owner.html", owner=owner, owner_repo_status=owner_repo_status)

@app.route('/<owner>/<repo>')
def get_owner_repo_page(owner, repo):
    # visitor = SubTreeNodeVisitor(1)
    # pre_order_travel_dict(bunch_dict, visitor)
    # cache_value['status'] = bunch_dict
    return render_template("owner_repo.html")