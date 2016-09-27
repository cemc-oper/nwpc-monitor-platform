# coding=utf-8
import datetime
from nwpc_monitor_web.app import app, redis_client, mongodb_client
from nwpc_work_flow_model.sms.visitor import pre_order_travel_dict, SubTreeNodeVisitor

from flask import json, request, jsonify,render_template, send_from_directory

nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop

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


@app.route('/')
def get_index_page():
    return render_template("index.html")


@app.route('/robots.txt')
def get_robots_txt_file():
    return render_template("robots.txt")


@app.route('/<no_static:owner>')
def get_owner_page(owner):
    repo_list = []
    if owner in owner_list:
        repo_list = owner_list[owner]['repos']

    owner_repo_status = []
    for a_repo in repo_list:
        a_repo_name = a_repo['name']
        cache_value = get_owner_repo_status(owner, a_repo_name)
        repo_status = None
        last_updated_time = None
        if cache_value is not None:
            bunch_dict = cache_value['status']

            repo_status = bunch_dict['status']
            time_string = cache_value['time']
            data_collect_datetime = datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S.%f")
            last_updated_time = data_collect_datetime.strftime('%Y-%m-%d %H:%M:%S')
        owner_repo_status.append({
            'owner': owner,
            'repo': a_repo_name,
            'status': repo_status,
            'last_updated_time': last_updated_time
        })

    return render_template("owner.html", owner=owner, owner_repo_status=owner_repo_status)


@app.route('/<no_static:owner>/<repo>')
@app.route('/<no_static:owner>/<repo>/')
@app.route('/<no_static:owner>/<repo>/status/head/')
def get_owner_repo_page(owner, repo):
    path = '/'
    last_updated_time = None
    children_status = []

    node_status = {
        'owner': owner,
        'repo': repo,
        'path': path,
        'last_updated_time': last_updated_time,
        'children': children_status
    }

    if owner not in owner_list:
        return render_template("owner_repo.html", owner=owner, repo=repo, node_status=node_status)

    found_repo = False
    for a_repo in owner_list[owner]['repos']:
        if repo == a_repo['name']:
            found_repo = True
            break
    if not found_repo:
        return render_template("owner_repo.html", owner=owner, repo=repo, node_status=node_status)

    cache_value = get_owner_repo_status(owner, repo)
    node_status = None
    if cache_value is not None:
        time_string = cache_value['time']
        data_collect_datetime = datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S.%f")
        last_updated_time = data_collect_datetime.strftime('%Y-%m-%d %H:%M:%S')

        bunch_dict = cache_value['status']
        visitor = SubTreeNodeVisitor(2)
        pre_order_travel_dict(bunch_dict, visitor)
        # cache_value['status'] = bunch_dict

        path = bunch_dict['path']

        children_status = []
        for a_suite in bunch_dict['children']:
            if len(a_suite['children']) > 0:
                has_children = True
            else:
                has_children = False
            children_status.append({
                'name': a_suite['name'],
                'path': a_suite['path'],
                'status': a_suite['status'],
                'has_children': has_children
            })

    node_status = {
        'owner': owner,
        'repo': repo,
        'path': path,
        'last_updated_time': last_updated_time,
        'children': children_status
    }

    return render_template("owner_repo.html", owner=owner, repo=repo, node_status=node_status)


@app.route('/<no_static:owner>/<repo>/status/head/<path:sms_path>', methods=['GET'])
def get_sms_status_page_by_path(owner, repo, sms_path):
    path = '/'
    last_updated_time = None
    children_status = []
    node_status = {
        'owner': owner,
        'repo': repo,
        'path': path,
        'last_updated_time': last_updated_time,
        'children': children_status
    }

    if owner not in owner_list:
        return render_template("owner_repo.html", owner=owner, repo=repo, node_status=node_status)

    found_repo = False
    for a_repo in owner_list[owner]['repos']:
        if repo == a_repo['name']:
            found_repo = True
            break
    if not found_repo:
        return render_template("owner_repo.html", owner=owner, repo=repo, node_status=node_status)

    cache_value = get_owner_repo_status(owner, repo)
    node_status = None
    if cache_value is not None:
        time_string = cache_value['time']
        data_collect_datetime = datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S.%f")
        last_updated_time = data_collect_datetime.strftime('%Y-%m-%d %H:%M:%S')

        bunch_dict = cache_value['status']

        def find_node(root, a_path):
            if a_path == '':
                return root
            tokens = a_path.split("/")
            cur_node = root
            parent_node = None
            for a_token in tokens:
                t_node = None
                for a_child_node in cur_node['children']:
                    if a_child_node['name'] == a_token:
                        t_node = a_child_node
                        break
                if t_node is None:
                    return None
                parent_node = cur_node
                cur_node = t_node
            return (cur_node, parent_node)
        node,p_node = find_node(bunch_dict, sms_path)
        if node is not None:
            children_status=[]
            if p_node:
                children_status.append(
                    {
                        'name': '..',
                        'path': p_node['path'],
                        'status': p_node['status'],
                        'has_children': True
                    }
                )
            path = node['path']
            for a_child in node['children']:
                if len(a_child['children']) > 0:
                    has_children = True
                else:
                    has_children = False
                children_status.append({
                    'name': a_child['name'],
                    'path': a_child['path'],
                    'status': a_child['status'],
                    'has_children': has_children
                })

    node_status = {
        'owner': owner,
        'repo': repo,
        'path': path,
        'last_updated_time': last_updated_time,
        'children': children_status
    }

    return render_template("owner_repo.html", owner=owner, repo=repo, node_status=node_status)


@app.route('/<no_static:owner>/<repo>/aborted_tasks/<int:id>', methods=['GET'])
def get_sms_aborted_tasks_page(id, owner, repo):
    aborted_tasks_content = {
        'update_time': None,
        'collected_time': None,
        'status_blob_id': None,
        'tasks': []
    }

    if owner not in owner_list:
        return render_template("aborted_tasks.html", owner=owner, repo=repo, aborted_tasks_content=aborted_tasks_content)

    found_repo = False
    for a_repo in owner_list[owner]['repos']:
        if repo == a_repo['name']:
            found_repo = True
            break
    if not found_repo:
        return render_template("aborted_tasks.html", owner=owner, repo=repo, aborted_tasks_content=aborted_tasks_content)

    blobs_collection = nwpc_monitor_platform_mongodb.blobs
    query_key = {
        'owner': owner,
        'repo': repo,
        'id': id
    }
    query_result = blobs_collection.find_one(query_key)
    if not query_result:
        return render_template("aborted_tasks.html", owner=owner, repo=repo, aborted_tasks_content=aborted_tasks_content)

    blob_content = query_result['data']['content']

    aborted_tasks_content = {
        'update_time': blob_content['update_time'],
        'collected_time': blob_content['collected_time'],
        'status_blob_id': blob_content['status_blob_id'],
        'tasks': blob_content['tasks']
    }

    return render_template("aborted_tasks.html", owner=owner, repo=repo, aborted_tasks_content=aborted_tasks_content)