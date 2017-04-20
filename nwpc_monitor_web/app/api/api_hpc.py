import gzip

from flask import request, json, jsonify, url_for

from nwpc_monitor_web.app.api import api_app
from nwpc_monitor_web.app.util import analytics, data_store


@api_app.route('/hpc/users/<user>/disk/usage', methods=['POST'])
def receive_disk_usage(user):
    content_encoding = request.headers.get('content-encoding', '').lower()
    if content_encoding == 'gzip':
        gzipped_data = request.data
        data_string = gzip.decompress(gzipped_data)
        body = json.loads(data_string.decode('utf-8'))
    else:
        body = request.form

    message = json.loads(body['message'])

    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    value = message
    data_store.save_disk_usage_to_mongodb(user, value)

    # send data to google analytics
    analytics.send_google_analytics_page_view(
        url_for('api_app.receive_disk_usage', user=user)
    )

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_app.route('/hpc/users/<user>/disk/usage', methods=['GET'])
def request_disk_usage(user):
    result = data_store.get_disk_usage_from_mongodb(user)
    return jsonify(result)


@api_app.route('/hpc/info/disk/space', methods=['POST'])
def receive_disk_space():
    content_encoding = request.headers.get('content-encoding', '').lower()
    if content_encoding == 'gzip':
        gzipped_data = request.data
        data_string = gzip.decompress(gzipped_data)
        body = json.loads(data_string.decode('utf-8'))
    else:
        body = request.form

    message = json.loads(body['message'])

    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    value = message
    data_store.save_disk_space_to_mongodb(value)

    # send data to google analytics
    analytics.send_google_analytics_page_view(
        url_for('api_app.receive_disk_space')
    )

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_app.route('/hpc/info/disk/space', methods=['GET'])
def request_disk_space():
    result = data_store.get_disk_space_from_mongodb()
    return jsonify(result)


@api_app.route('/hpc/users/<user>/loadleveler/status', methods=['POST'])
def receive_loadleveler_status(user):
    content_encoding = request.headers.get('content-encoding', '').lower()
    if content_encoding == 'gzip':
        gzipped_data = request.data
        data_string = gzip.decompress(gzipped_data)
        body = json.loads(data_string.decode('utf-8'))
    else:
        body = request.form

    message = json.loads(body['message'])

    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    value = message
    data_store.save_hpc_loadleveler_status_to_cache(user, value)

    # send data to google analytics
    analytics.send_google_analytics_page_view(
        url_for('api_app.receive_loadleveler_status', user=user)
    )

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_app.route('/hpc/users/<user>/loadleveler/status', methods=['GET'])
def request_loadleveler_status(user):
    result = data_store.get_hpc_loadleveler_status_from_cache(user)
    return jsonify(result)
