# coding=utf-8
from flask import Blueprint, request, json, jsonify
from nwpc_monitor_web import app

import redis

redis_host = app.config['NWPC_MONITOR_WEB_CONFIG']['redis']['host']['ip']
redis_port = app.config['NWPC_MONITOR_WEB_CONFIG']['redis']['host']['port']
redis_client = redis.Redis(host=redis_host, port=redis_port)

api_app = Blueprint('api_app', __name__, template_folder='template')

@api_app.route('/repos/<owner>/<repo>/sms/<sms_name>/status', methods=['POST'])
def get_sms_status(owner, repo, sms_name):
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

    # 保存到本地缓存
    key = "{owner}/{repo}/sms/{sms_name}/status".format(owner=owner, repo=repo, sms_name=sms_name)
    redis_client.set(key, json.dumps(message))
    result = {
        'status': 'ok'
    }
    return jsonify(result)