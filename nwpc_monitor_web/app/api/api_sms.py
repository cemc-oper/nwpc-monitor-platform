from flask import request, json, jsonify, url_for
import requests

from nwpc_work_flow_model.sms.visitor import SubTreeNodeVisitor, pre_order_travel_dict
from nwpc_monitor_web.app.api import api_app
from nwpc_monitor_web.app import app, redis_client, mongodb_client

# mongodb
nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status


@api_app.route('/repos/<owner>/<repo>/sms/status', methods=['POST'])
def post_sms_status(owner, repo):

    r = request
    message = json.loads(request.form['message'])
    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)

    if message['data']['type'] == 'status':
        redis_value = message['data']

        redis_value['type'] = 'sms'

        # 保存到本地缓存
        """
        redis_value:
        {
            "name": "sms_status_message_data",
            "type": "record",
            "fields": [
                {"name": "owner", "type": "string"},
                {"name": "repo", "type": "string"},
                {"name": "sms_name", "type": "string"},
                {"name": "time", "type": "string"},
                {
                    "name": "status",
                    "doc": "bunch status dict",
                    "type": { "type": "node" }
                }
            ]
        }
        """
        redis_client.set(key, json.dumps(redis_value))

    elif message['data']['type'] == 'takler_object':
        status_blob = None
        aborted_blob = None
        for a_blob in message['data']['blobs']:
            if a_blob['data']['type'] == 'status':
                status_blob = a_blob
            if a_blob['data']['type'] == 'aborted_tasks':
                aborted_blob = a_blob
        if status_blob is None:
            result = {
                'status': 'error',
                'message': 'can\'t find a status blob.'
            }
            return jsonify(result)

        tree_object = message['data']['trees'][0]
        commit_object = message['data']['commits'][0]

        # 保存到本地缓存
        redis_value = {
            'owner': owner,
            'repo': repo,
            'sms_name': repo,
            'time': status_blob['data']['content']['collected_time'],
            'status': status_blob['data']['content']['status'],
            'type': 'sms'
        }
        redis_client.set(key, json.dumps(redis_value))

        # 保存到 mongodb
        blobs_collection = nwpc_monitor_platform_mongodb.blobs
        blobs_collection.insert_one(status_blob)
        if aborted_blob:
            blobs_collection.insert_one(aborted_blob)

        trees_collection = nwpc_monitor_platform_mongodb.trees
        trees_collection.insert_one(tree_object)

        commits_collection = nwpc_monitor_platform_mongodb.commits
        commits_collection.insert_one(commit_object)

    # send data to google analytics
    google_analytics_config = app.config['NWPC_MONITOR_WEB_CONFIG']['analytics']['google_analytics']
    if google_analytics_config['enable'] is True:
        post_data = {
            'v': google_analytics_config['version'],
            't': 'pageview',
            'tid': google_analytics_config['track_id'],
            'cid': google_analytics_config['client_id'],
            'dh': google_analytics_config['document_host'],
            'dp': url_for('api_app.post_sms_status', owner=owner, repo=repo)
        }
        requests.post(google_analytics_config['url'], data=post_data)

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_app.route('/repos/<owner>/<repo>/sms/status', methods=['GET'])
def get_sms_status(owner, repo):
    r = request
    args = request.args

    depth = -1
    if 'depth' in args:
        depth = int(args['depth'])

    # 保存到本地缓存
    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
    message_string = redis_client.get(key)
    message = json.loads(message_string)

    """
    message:
    {
        "name": "sms_status_message_data",
        "type": "record",
        "fields": [
            {"name": "owner", "type": "string"},
            {"name": "repo", "type": "string"},
            {"name": "sms_name", "type": "string"},
            {"name": "time", "type": "string"},
            {"name": "type", "type": "enum", "symbols": ["sms"]},
            {
                "name": "status",
                "doc": "bunch status dict",
                "type": { "type": "node" }
            }
        ]
    }
    """

    bunch_dict = message['status']
    visitor = SubTreeNodeVisitor(depth)
    pre_order_travel_dict(bunch_dict, visitor)

    message['status'] = bunch_dict

    # send data to google analytics
    google_analytics_config = app.config['NWPC_MONITOR_WEB_CONFIG']['analytics']['google_analytics']
    if google_analytics_config['enable'] is True:
        post_data = {
            'v': google_analytics_config['version'],
            't': 'pageview',
            'tid': google_analytics_config['track_id'],
            'cid': google_analytics_config['client_id'],
            'dh': google_analytics_config['document_host'],
            'dp': url_for('api_app.get_sms_status', owner=owner, repo=repo)
        }
        requests.post(google_analytics_config['url'], data=post_data)


    result = {
        'status': 'ok',
        'data': message
    }
    return jsonify(result)