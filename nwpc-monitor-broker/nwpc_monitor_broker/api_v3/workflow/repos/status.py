# coding=utf-8

import datetime
import gzip

import requests
from flask import request, jsonify, json

from nwpc_monitor_broker.api_v3 import api_v3_app

from nwpc_monitor_broker.common.workflow.sms import sms_status_message_handler


@api_v3_app.route('/workflow/repos/<owner>/<repo>/status', methods=['POST'])
def receive_sms_status_message(owner, repo):
    """
    接收外部发送来的 SMS 服务器的状态，将其保存到本地缓存，并发送到外网服务器
    :return:
    """
    start_time = datetime.datetime.utcnow()

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

    message_data = message['data']
    sms_status_message_handler(message_data)

    result = {
        'status': 'ok'
    }
    end_time = datetime.datetime.utcnow()
    print(end_time - start_time)

    return jsonify(result)
