# coding=utf-8
from datetime import datetime
import requests
from flask import json

from .cache import save_weixin_access_token_to_cache, get_weixin_access_token_from_cache
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
        if 'errcode' in response_json:
            result = {
                'status': 'error',
                'errcode': response_json['errcode'],
                'errmsg': response_json['errmsg']
            }
        else:
            access_token = response_json['access_token']
            save_weixin_access_token_to_cache(access_token)
            result = {
                'status': 'ok',
                'access_token': access_token
            }
        return result

    def get_access_token_from_cache(self) -> str:
        return get_weixin_access_token_from_cache()

    def save_access_token_to_cache(self, access_token: str) -> None:
        return save_weixin_access_token_to_cache(access_token)

    def get_access_token(self) -> str:
        weixin_access_token = get_weixin_access_token_from_cache()
        if weixin_access_token is None:
            self.get_access_token_from_server()
            weixin_access_token = get_weixin_access_token_from_cache()
        return weixin_access_token


class WeixinApp(object):
    def __init__(self, weixin_config:dict, cloud_config:dict):
        self.weixin_config = weixin_config
        self.cloud_config = cloud_config

        self.auth = Auth(self.weixin_config['token'])


    def send_warning_message(self, owner:str, repo:str, sms_server_name:str, suite_error_map:dict, message_datetime:datetime):
        print('Get new error task. Pushing warning message to weixin...')

        auth = Auth(self.weixin_config['token'])
        weixin_access_token = auth.get_access_token()

        warning_post_url = self.weixin_config['warn']['url'].format(
            weixin_access_token=weixin_access_token
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
            "touser":"wangdp",
            "agentid": self.weixin_config['warn']['agentid'],
            "msgtype":"text",
            "text": {
                "content":"业务系统运行出错\n" +
                    "{sms_server_name}，请查看\n出错 suite 列表：\n".format(sms_server_name=sms_server_name) +
                    "日期 : {error_date}\n".format(error_date=message_datetime.strftime("%Y-%m-%d")) +
                    "时间 : {error_time}".format(error_time=message_datetime.strftime("%H:%M:%S"))
            }
        }
        for a_suite in form_suite_error_list:
            warning_post_message['text']['content'] += "\n" + a_suite['name'] + ' : ' + str(a_suite['count'])

        warning_post_message['text']['content'] += "\n" + self.cloud_config['base']['url']

        warning_post_headers = {
            'content-type': 'application/json'
        }
        warning_post_data = json.dumps(warning_post_message,ensure_ascii=False).encode('utf8')

        result = requests.post(warning_post_url,
                               data=warning_post_data,
                               verify=False,
                               headers=warning_post_headers)
        print(result.json())
