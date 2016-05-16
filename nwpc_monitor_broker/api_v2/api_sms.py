# coding=utf-8

from nwpc_monitor_broker import app
from nwpc_monitor_broker.api_v2 import api_v2_app, redis_client
from nwpc_monitor_broker.nwpc_log import Node, Bunch
from flask import request, json, jsonify
import requests


WARING_POST_URL = app.config['BROKER_CONFIG']['app']['warn']['url']

@api_v2_app.route('/hpc/sms/status', methods=['POST'])
def receive_sms_status():
    """
    接收外部发送来的 SMS 服务器的状态，将其保存到本地缓存，并发送到外网服务器
    :return:
    """
    message = json.loads(request.form['message'])

    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    message_data = message['data']
    sms_name = message_data['sms_name']
    sms_user = message_data['sms_user']

    bunch_dict = message_data['status']

    # 检测是否需要推送警告信息
    key = "hpc/sms/{sms_user}/{sms_name}/status".format(sms_user=sms_user, sms_name=sms_name)
    print key
    # 获取服务器'/' 的状态
    if len(bunch_dict) >0:
        print 'building bunch from message...'
        bunch = Bunch.create_from_dict(bunch_dict)
        print 'building bunch from message...Done'
        server_status = bunch.status # TODO：使用循环查找
        if server_status == 'abo':
            cached_message_string = redis_client.get(key)
            if cached_message_string is not None:
                cached_message = json.loads(cached_message_string)
                print 'building bunch from cache...'
                cached_bunch = Bunch.create_from_dict(cached_message['status'])
                print 'building bunch from cache...Done'
                previous_server_status = cached_bunch.status
                if previous_server_status != 'abo':
                    # 发送推送警告
                    print 'Get aborted. Pushing warning message...'

    # 保存到本地缓存
    print "Saving message to cache..."
    cached_value = json.dumps(message_data)
    print "len of cached value: ", len(cached_value)
    redis_client.set(key, cached_value)
    print "Saving message to cache...Done"

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_v2_app.route('/dingtalk/access_token/get', methods=['GET'])
def get_dingtalk_access_token():
    key = "dingtalk_access_token"

    corp_id = app.config['BROKER_CONFIG']['app']['token']['corp_id']
    corp_secret = app.config['BROKER_CONFIG']['app']['token']['corp_secret']

    headers = {'content-type': 'application/json'}
    url = app.config['BROKER_CONFIG']['app']['token']['url'].format(
        corp_id=corp_id, corp_secret=corp_secret
    )

    token_response = requests.get(url,verify=False, headers=headers)
    response_json = token_response.json()
    print response_json
    if response_json['errcode'] == 0:
        # 更新 token
        access_token = response_json['access_token']
        redis_client.set(key, access_token)
        result = {
            'status': 'ok',
            'access_token': access_token
        }
    else:
        result = {
            'status': 'error',
            'errcode': response_json['errcode']
        }
    print result
    return jsonify(result)