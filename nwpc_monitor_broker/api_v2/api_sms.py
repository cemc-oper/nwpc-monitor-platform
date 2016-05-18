# coding=utf-8
import datetime

from nwpc_monitor_broker import app
from nwpc_monitor_broker.api_v2 import api_v2_app, redis_client, mongodb_client
from nwpc_monitor_broker.nwpc_log import Bunch
from flask import request, json, jsonify
import requests


nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status

def get_sms_server_status_from_cache(owner, repo, sms_name, sms_user):

    key = {
        'owner': owner,
        'repo': repo,
        'sms_name': sms_name,
        'sms_user': sms_user
    }

    result = sms_server_status.find_one(key)

    return result

def save_sms_server_status_to_cache(owner, repo, sms_name, sms_user, message):
    key = {
        'owner': owner,
        'repo': repo,
        'sms_name': sms_name,
        'sms_user': sms_user
    }
    value = {
        'owner': owner,
        'repo': repo,
        'sms_name': sms_name,
        'sms_user': sms_user,
        'update_time': datetime.datetime.now(),
        'collected_time': message['time'],
        'status': message['status']
    }
    sms_server_status.update(key, value, upsert=True)
    return


@api_v2_app.route('/hpc/sms/status', methods=['POST'])
def sms_status_message_handler():
    """
    接收外部发送来的 SMS 服务器的状态，将其保存到本地缓存，并发送到外网服务器
    :return:
    """
    start_time = datetime.datetime.now()
    message = json.loads(request.form['message'])

    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    message_data = message['data']
    owner = message_data['owner']
    repo = message_data['repo']
    sms_name = message_data['sms_name']
    sms_user = message_data['sms_user']

    bunch_dict = message_data['status']

    key = "hpc/sms/{sms_user}/{sms_name}/status".format(sms_user=sms_user, sms_name=sms_name)
    print key
    if len(bunch_dict) >0:

        print 'building bunch from message...'
        bunch = Bunch.create_from_dict(bunch_dict)
        print 'building bunch from message...Done'

        server_status = bunch.status

        if server_status == 'abo':
            cached_sms_server_status = get_sms_server_status_from_cache(owner, repo, sms_name, sms_user)
            if cached_sms_server_status is not None:

                print 'building bunch from cache message...'
                cached_bunch = Bunch.create_from_dict(cached_sms_server_status['status'])
                print 'building bunch from cache message...Done'

                previous_server_status = cached_bunch.status

                if previous_server_status != 'abo':
                    print 'Get aborted. Pushing warning message...'

                    # get access token
                    access_token_key = "dingtalk_access_token"
                    dingtalk_access_token = redis_client.get(access_token_key)
                    if dingtalk_access_token is None:
                        get_dingtalk_access_token()
                        dingtalk_access_token = redis_client.get(access_token_key)

                    sms_server_name=cached_bunch.name
                    error_datetime = datetime.datetime.strptime(message_data['time'], "%Y-%m-%dT%H:%M:%S.%f")

                    warning_post_url = app.config['BROKER_CONFIG']['app']['warn']['url'].format(
                        dingtalk_access_token=dingtalk_access_token
                    )
                    warning_post_message = {
                        "touser":"manager4941",
                        "agentid":"4078086",
                        "msgtype":"oa",
                        "oa": {
                            "message_url": app.config['BROKER_CONFIG']['cloud']['base']['url'],
                            "head": {
                                "bgcolor": "ffff0000",
                                "text": "业务系统报警"
                            },
                            "body":{
                                "title":"业务系统运行出错",
                                "content":"{sms_server_name} 出错，请查看".format(sms_server_name=sms_server_name),
                                "form":[
                                    {
                                        "key": "{sms_server_name} : ".format(sms_server_name=sms_server_name),
                                        "value": "aborted"
                                    },
                                    {
                                        "key": "日期 : ",
                                        "value": "{error_date}".format(error_date=error_datetime.strftime("%Y-%m-%d"))
                                    },
                                    {
                                        "key": "时间 : ",
                                        "value": "{error_time}".format(error_time=error_datetime.strftime("%H:%M:%S"))
                                    }
                                ]
                            }
                        }
                    }
                    warning_post_headers = {'content-type': 'application/json'}
                    warning_post_data = json.dumps(warning_post_message)

                    result = requests.post(warning_post_url,
                                           data=warning_post_data,
                                           verify=False,
                                           headers=warning_post_headers)
                    print result.json()

    # save to cache
    save_sms_server_status_to_cache(owner, repo, sms_name, sms_user, message_data)

    result = {
        'status': 'ok'
    }
    end_time = datetime.datetime.now()
    print end_time - start_time

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