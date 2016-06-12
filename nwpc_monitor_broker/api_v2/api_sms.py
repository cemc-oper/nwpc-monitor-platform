# coding=utf-8

from flask import request, jsonify, json
import datetime
import requests

from nwpc_monitor_broker import app

from nwpc_monitor_broker.api_v2 import api_v2_app
from nwpc_monitor_broker.api_v2 import cache
from nwpc_monitor_broker.api_v2 import data_store
from nwpc_monitor_broker.api_v2 import ding_talk, weixin

from nwpc_monitor.nwpc_log import Bunch, ErrorStatusTaskVisitor, pre_order_travel



def is_new_abort_task_found(owner:str, repo:str, previous_server_status:str, error_task_dict_list:list):
    new_error_task_found = True

    if previous_server_status == 'abo':
        new_error_task_found = False
        cached_error_task_value = cache.get_error_task_list_from_cache(owner, repo)
        cached_error_task_name_list = [a_task_item['path'] for a_task_item in
                                       cached_error_task_value['error_task_list'] ]
        for a_task in error_task_dict_list:
            if a_task['path'] not in cached_error_task_name_list:
                new_error_task_found = True
                break

    return new_error_task_found


def is_new_abort_root_found(owner:str, repo:str, previous_server_status:str, current_server_status:str='abo'):
    if previous_server_status != 'abo' and current_server_status == 'abo':
        return True
    else:
        return False


"""
message_data:
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
                "doc": "bunch status",
                "type": { "type": "node" }
            }
        ]
    }
"""
def sms_status_message_handler(message_data: dict) -> None:
    owner = message_data['owner']
    repo = message_data['repo']
    sms_name = message_data['sms_name'] # sms_name 应该与 repo 一致
    #sms_user = message_data['sms_user']
    message_time = message_data['time']

    bunch_dict = message_data['status']
    message_datetime = datetime.datetime.strptime(message_time, "%Y-%m-%dT%H:%M:%S.%f")

    warn_user_list = data_store.get_ding_talk_warn_user_list(owner, repo)

    sms_server_key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
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
            cached_sms_server_status = cache.get_sms_server_status_from_cache(owner, repo, sms_name)
            if cached_sms_server_status is not None:

                print('building bunch from cache message...')
                cached_bunch = Bunch.create_from_dict(cached_sms_server_status['status'])
                print('building bunch from cache message...Done')

                previous_server_status = cached_bunch.status

                #if True:
                if is_new_abort_task_found(owner, repo, previous_server_status, error_task_dict_list):
                    warning_data = {
                        'owner': owner,
                        'repo': repo,
                        'sms_server_name': sms_name, # bunch.name
                        'message_datetime': message_datetime,
                        'suite_error_map': suite_error_map
                    }

                    ding_talk_app = ding_talk.DingTalkApp(
                        ding_talk_config=app.config['BROKER_CONFIG']['ding_talk_app'],
                        cloud_config=app.config['BROKER_CONFIG']['cloud']
                    )

                    ding_talk_app.send_warning_message(warning_data)

                    weixin_app = weixin.WeixinApp(
                        weixin_config=app.config['BROKER_CONFIG']['weixin_app'],
                        cloud_config=app.config['BROKER_CONFIG']['cloud']
                    )
                    weixin_app.send_warning_message(warning_data)

        # 保存 error_task_list 到缓存
        error_task_value = {
            'timestamp': datetime.datetime.now(),
            'error_task_list': error_task_dict_list
        }
        cache.save_error_task_list_to_cache(owner, repo, error_task_value)

        cache.save_sms_server_status_to_cache(owner, repo, sms_name, message_data)

        # 发送给外网服务器
        website_url = app.config['BROKER_CONFIG']['cloud']['put']['url'].format(
            owner=owner,
            repo=repo
        )
        website_post_data = {
            'message': json.dumps(message_data)
        }
        response = requests.post(website_url, data=website_post_data)
        print(response)
        return


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
    auth = ding_talk.Auth(app.config['BROKER_CONFIG']['ding_talk_app']['token'])
    result = auth.get_access_token_from_server()
    print(result)
    return jsonify(result)

@api_v2_app.route('/weixin/access_token/get', methods=['GET'])
def get_weixin_access_token():
    auth = weixin.Auth(app.config['BROKER_CONFIG']['weixin_app']['token'])
    result = auth.get_access_token_from_server()
    print(result)
    return jsonify(result)