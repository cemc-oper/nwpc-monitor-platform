# coding=utf-8
import datetime

from flask import request, json, jsonify
import requests

from nwpc_monitor_broker import app
from nwpc_monitor_broker.api_v2 import api_v2_app, redis_client, mongodb_client

from nwpc_monitor_broker.nwpc_log import Bunch, ErrorStatusTaskVisitor, pre_order_travel


nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status

def get_sms_server_status_from_cache(owner, repo, sms_name):

    key = {
        'owner': owner,
        'repo': repo,
        'sms_name': sms_name
    }

    result = sms_server_status.find_one(key)

    return result

def save_sms_server_status_to_cache(owner, repo, sms_name, message):
    key = {
        'owner': owner,
        'repo': repo,
        'sms_name': sms_name
    }
    value = {
        'owner': owner,
        'repo': repo,
        'sms_name': sms_name,
        'update_time': datetime.datetime.now(),
        'collected_time': message['time'],
        'status': message['status']
    }
    sms_server_status.update(key, value, upsert=True)
    return


def get_access_token_from_cache():
    access_token_key = "dingtalk_access_token"
    dingtalk_access_token = redis_client.get(access_token_key)
    if dingtalk_access_token is None:
        get_dingtalk_access_token()
        dingtalk_access_token = redis_client.get(access_token_key)
    return dingtalk_access_token


def sms_status_message_handler(message_data):
    owner = message_data['owner']
    repo = message_data['repo']
    sms_name = message_data['sms_name']
    #sms_user = message_data['sms_user']
    message_time = message_data['time']

    bunch_dict = message_data['status']
    message_datetime = datetime.datetime.strptime(message_time, "%Y-%m-%dT%H:%M:%S.%f")

    sms_server_key = "{owner}/{repo}/{sms_name}".format(owner=owner, repo=repo, sms_name=sms_name)
    error_task_key = "{owner}/{repo}/{sms_name}/task/error".format(owner=owner, repo=repo, sms_name=sms_name)
    print(sms_server_key)

    if len(bunch_dict) >0:
        print('building bunch from message...')
        bunch = Bunch.create_from_dict(bunch_dict)
        print('building bunch from message...Done')

        # find error tasks every suite
        suite_error_map = dict()
        error_task_dict_list = []
        for a_suite in bunch.children:
            error_visitor = ErrorStatusTaskVisitor()
            pre_order_travel(a_suite, error_visitor)
            suite_error_map[a_suite.name] = {
                'name': a_suite.name,
                'status': a_suite.status,
                'error_task_list': error_visitor.error_task_list
            }
            for a_task in error_visitor.error_task_list:
                 error_task_dict_list.append(a_task.to_dict())

        server_status = bunch.status

        if server_status == 'abo':
            cached_sms_server_status = get_sms_server_status_from_cache(owner, repo, sms_name)
            if cached_sms_server_status is not None:

                print('building bunch from cache message...')
                cached_bunch = Bunch.create_from_dict(cached_sms_server_status['status'])
                print('building bunch from cache message...Done')

                previous_server_status = cached_bunch.status

                new_error_task_found = True
                if previous_server_status == 'abo':
                    new_error_task_found = False
                    cached_error_task_value = json.loads(redis_client.get(error_task_key))
                    cached_error_task_name_list = [a_task_item['path'] for a_task_item in
                                                   cached_error_task_value['error_task_list'] ]
                    for a_task in error_task_dict_list:
                        if a_task['path'] not in cached_error_task_name_list:
                            new_error_task_found = True
                            break

                if new_error_task_found:
                    print('Get new error task. Pushing warning message...')

                    dingtalk_access_token = get_access_token_from_cache()

                    sms_server_name=bunch.name

                    warning_post_url = app.config['BROKER_CONFIG']['app']['warn']['url'].format(
                        dingtalk_access_token=dingtalk_access_token
                    )

                    form_suite_error_list = []
                    for a_suite_name in suite_error_map:
                        a_suite_item = suite_error_map[a_suite_name]
                        if len(a_suite_item['error_task_list']) > 0:
                            form_suite_error_list.append({
                                'name': a_suite_item['name'],
                                'count': len(a_suite_item['error_task_list'])
                            })

                    warning_post_message = {
                        "touser":"manager4941",
                        "agentid": app.config['BROKER_CONFIG']['app']['warn']['agentid'],
                        "msgtype":"oa",
                        "oa": {
                            "message_url": app.config['BROKER_CONFIG']['cloud']['base']['url'],
                            "head": {
                                "bgcolor": "ffff0000",
                                "text": "业务系统报警"
                            },
                            "body":{
                                "title":"业务系统运行出错",
                                "content":"{sms_server_name} 出错，请查看\n出错 suite 列表：".format(sms_server_name=sms_server_name),
                                "form":[
                                    {
                                        "key": "日期 : ",
                                        "value": "{error_date}".format(error_date=message_datetime.strftime("%Y-%m-%d"))
                                    },
                                    {
                                        "key": "时间 : ",
                                        "value": "{error_time}".format(error_time=message_datetime.strftime("%H:%M:%S"))
                                    }
                                ]
                            }
                        }
                    }
                    for a_suite in form_suite_error_list:
                        warning_post_message['oa']['body']['form'].insert(0, {
                            'key': a_suite['name'] + ' : ',
                            'value': a_suite['count']
                        })

                    warning_post_headers = {'content-type': 'application/json'}
                    warning_post_data = json.dumps(warning_post_message)

                    result = requests.post(warning_post_url,
                                           data=warning_post_data,
                                           verify=False,
                                           headers=warning_post_headers)
                    print(result.json())

        error_task_value = {
            'timestamp': datetime.datetime.now(),
            'error_task_list': error_task_dict_list
        }
        redis_client.set(error_task_key, json.dumps(error_task_value))

        save_sms_server_status_to_cache(owner, repo, sms_name, message_data)


@api_v2_app.route('/hpc/sms/status', methods=['POST'])
def receive_sms_status_message():
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
    sms_status_message_handler(message_data)

    result = {
        'status': 'ok'
    }
    end_time = datetime.datetime.now()
    print(end_time - start_time)

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
    print(response_json)
    if response_json['errcode'] == 0:
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
    print(result)
    return jsonify(result)