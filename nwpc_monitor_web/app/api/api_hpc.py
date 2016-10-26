from flask import request, json, jsonify, url_for
import requests

from nwpc_monitor_web.app.api import api_app, data_store
from nwpc_monitor_web.app import app


@api_app.route('/hpc/users/<user>/disk-usage', methods=['POST'])
def receive_disk_usage(user):

    message = json.loads(request.form['message'])

    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    value = message
    data_store.save_disk_usage_to_mongodb(user, value)

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_app.route('/hpc/users/<user>/disk-usage', methods=['GET'])
def request_disk_usage(user):
    result = data_store.get_disk_usage_to_mongodb(user)
    return jsonify(result)
