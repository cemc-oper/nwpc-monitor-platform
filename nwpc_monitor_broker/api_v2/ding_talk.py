# coding=utf-8
from datetime import datetime
import requests
from flask import json

from .cache import save_dingtalk_access_token_to_cache, get_dingtalk_access_token_from_cache
from nwpc_monitor_broker.api_v2 import data_store

class Auth(object):
    """
    config:
        {
            "name": "TokenConfig",
            "type": "record",
            "fields": [
                {"name": "corp_id", type: "string"},
                {"name": "corp_secret", type: "string"},
                {"name": "url", type: "string"},
            ]
        }
    """
    def __init__(self, config: dict):
        self.corp_id = config['corp_id']
        self.corp_secret = config['corp_secret']
        self.url = config['url']

    def get_access_token_from_server(self) -> dict:
        headers = {'content-type': 'application/json'}
        url = self.url.format(
            corp_id=self.corp_id, corp_secret=self.corp_secret
        )

        token_response = requests.get(url,verify=False, headers=headers)

        response_json = token_response.json()
        print(response_json)
        if response_json['errcode'] == 0:
            access_token = response_json['access_token']
            save_dingtalk_access_token_to_cache(access_token)
            result = {
                'status': 'ok',
                'access_token': access_token
            }
        else:
            result = {
                'status': 'error',
                'errcode': response_json['errcode']
            }
        return result

    def get_access_token_from_cache(self) -> str:
        return get_dingtalk_access_token_from_cache()

    def save_access_token_to_cache(self, access_token: str) -> None:
        return save_dingtalk_access_token_to_cache(access_token)

    def get_access_token(self) -> str:
        dingtalk_access_token = get_dingtalk_access_token_from_cache()
        if dingtalk_access_token is None:
            self.get_access_token_from_server()
            dingtalk_access_token = get_dingtalk_access_token_from_cache()
        return dingtalk_access_token


class DingTalkApp(object):
    def __init__(self, ding_talk_config:dict, cloud_config:dict):
        self.ding_talk_config = ding_talk_config
        self.cloud_config = cloud_config

        self.auth = Auth(self.ding_talk_config['token'])


    def send_warning_message(self, owner:str, repo:str, sms_server_name:str, suite_error_map:dict, message_datetime:datetime):
        warn_user_list = data_store.get_warn_user_list(owner, repo)

        print('Get new error task. Pushing warning message...')

        auth = Auth(self.ding_talk_config['token'])
        dingtalk_access_token = auth.get_access_token()

        warning_post_url = self.ding_talk_config['warn']['url'].format(
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
            "touser":"|".join(warn_user_list),
            "agentid": self.ding_talk_config['warn']['agentid'],
            "msgtype":"oa",
            "oa": {
                "message_url": self.cloud_config['base']['url'],
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
