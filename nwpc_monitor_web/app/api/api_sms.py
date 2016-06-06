from flask import request, json, jsonify

from nwpc_monitor.nwpc_log.visitor import SubTreeNodeVisitor, pre_order_travel_dict
from nwpc_monitor_web.app import api_app
from nwpc_monitor_web.app import redis_client


@api_app.route('/repos/<owner>/<repo>/sms/status', methods=['POST'])
def post_sms_status(owner, repo):
    r = request
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
            {
                "name": "status",
                "doc": "bunch status dict",
                "type": { "type": "node" }
            }
        ]
    }
    """
    message = json.loads(request.form['message'])
    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    message['type'] = 'sms'

    # 保存到本地缓存
    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
    redis_client.set(key, json.dumps(message))
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

    result = {
        'status': 'ok',
        'data': message
    }
    return jsonify(result)