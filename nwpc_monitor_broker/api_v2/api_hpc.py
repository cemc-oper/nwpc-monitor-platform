from flask import request, jsonify, json
import datetime
import requests

from nwpc_monitor_broker import app

from nwpc_monitor_broker.api_v2 import api_v2_app
from nwpc_monitor_broker.api_v2 import cache


@api_v2_app.route('/hpc/users/<user>/disk-usage', methods=['POST'])
def receive_disk_usage_message(user):
    start_time = datetime.datetime.now()
    message = json.loads(request.form['message'])

    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    message_data = message['data']

    key, value = cache.save_hpc_disk_usage_status_from_cache(user, message)

    print("post disk usage to cloud: user=", user)
    post_data = {
        'message': json.dumps(value)
    }
    post_url = app.config['BROKER_CONFIG']['hpc']['disk_usage']['cloud']['put']['url'].format(
        user=user
    )
    response = requests.post(post_url, data=post_data)
    print("post disk usage to cloud done: response=", response)

    result = {
        'status': 'ok'
    }
    end_time = datetime.datetime.now()
    print(end_time - start_time)

    return jsonify(result)


@api_v2_app.route('/hpc/users/<user>/disk-usage', methods=['GET'])
def get_disk_usage_message(user: str):
    start_time = datetime.datetime.now()

    result = cache.get_hpc_disk_usage_status_from_cache(user)

    end_time = datetime.datetime.now()
    print(end_time - start_time)

    return jsonify(result)