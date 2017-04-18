# coding=utf-8
from datetime import datetime
import requests
from flask import json

from .cache import save_weixin_access_token_to_cache, get_weixin_access_token_from_cache
from nwpc_monitor_broker.api_v2 import data_store

REQUEST_POST_TIME_OUT = 60


class Auth(object):
    def __init__(self, config: dict):
        """
        :param config:
            {
                "name": "TokenConfig",
                "type": "record",
                "fields": [
                    {"name": "corp_id", type: "string"},
                    {"name": "corp_secret", type: "string"},
                    {"name": "url", type: "string"},
                ]
            }
        :return:
        """

        self.corp_id = config['corp_id']
        self.corp_secret = config['corp_secret']
        self.url = config['url']

    def get_access_token_from_server(self) -> dict:
        headers = {'content-type': 'application/json'}
        url = self.url.format(
            corp_id=self.corp_id, corp_secret=self.corp_secret
        )

        token_response = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=REQUEST_POST_TIME_OUT
        )

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

    def send_warning_message(self, warning_data:dict):
        """
        :param warning_data:
            {
                "name": "WarningData",
                "namespace": "WeixinApp",
                "type": "record",
                "fields": [
                    {"name": "owner", type: "string"},
                    {"name": "repo", type: "string"},
                    {"name": "sms_server_name", type: "string"},
                    {"name": "message_datetime", type: "datetime"},
                    {"name": "suite_error_map", type: "array"},
                    {"name": "aborted_tasks_blob_id", type: "int"},
                ]
            }
        :return:
        """
        print('Get new error task. Pushing warning message to weixin...')

        auth = Auth(self.weixin_config['token'])
        weixin_access_token = auth.get_access_token()

        warning_post_url = self.weixin_config['warn']['url'].format(
            weixin_access_token=weixin_access_token
        )

        if warning_data['aborted_tasks_blob_id']:
            message_url = (self.cloud_config['base']['url'] + '/{owner}/{repo}/aborted_tasks/{id}').format(
                owner=warning_data['owner'],
                repo=warning_data['repo'],
                id=warning_data['aborted_tasks_blob_id']
            )
        else:
            message_url = self.cloud_config['base']['url']

        form_suite_error_list = []
        for a_suite_name in warning_data['suite_error_map']:
            a_suite_item = warning_data['suite_error_map'][a_suite_name]
            if len(a_suite_item['error_task_list']) > 0:
                form_suite_error_list.append({
                    'name': a_suite_item['name'],
                    'count': len(a_suite_item['error_task_list'])
                })

        warning_post_message = {
            "touser":"@all",
            "agentid": self.weixin_config['warn']['agentid'],
            "msgtype":"text",
            "text": {
                "content":"业务系统运行出错\n" +
                    "{sms_server_name}，请查看\n出错 suite 列表：\n".format(sms_server_name=warning_data['sms_server_name']) +
                    "日期 : {error_date}\n".format(error_date=warning_data['message_datetime'].strftime("%Y-%m-%d")) +
                    "时间 : {error_time}".format(error_time=warning_data['message_datetime'].strftime("%H:%M:%S"))
            }
        }
        for a_suite in form_suite_error_list:
            warning_post_message['text']['content'] += "\n" + a_suite['name'] + ' : ' + str(a_suite['count'])

        warning_post_message['text']['content'] += '\n<a href=\"' + message_url + '">查看详情</a>'

        warning_post_headers = {
            'content-type': 'application/json'
        }
        warning_post_data = json.dumps(warning_post_message,ensure_ascii=False).encode('utf8')

        result = requests.post(
            warning_post_url,
            data=warning_post_data,
            verify=False,
            headers=warning_post_headers,
            timeout=REQUEST_POST_TIME_OUT
        )
        print(result.json())

    def send_sms_node_task_warn(self, warning_data):
        auth = Auth(self.weixin_config['token'])
        weixin_access_token = auth.get_access_token()

        warning_post_url = self.weixin_config['warn']['url'].format(
            weixin_access_token=weixin_access_token
        )

        node_list_content = ''
        for a_unfit_node in warning_data['data']['unfit_nodes']:
            node_list_content += a_unfit_node['node_path'] + ' : ' + str(
                len(a_unfit_node['unfit_variables'])) + "\n"

        articles = [
            {
                'title': "业务系统异常：SMS节点状态",
                "picurl": "http://wx2.sinaimg.cn/mw690/4afdac38ly1feqnwb44kkj2223112wfj.jpg"
            },
            {
                "title": "{owner}/{repo}".format(
                    owner=warning_data['data']['owner'],
                    repo=warning_data['data']['repo']
                ),
                "description": warning_data['data']['task_name']
            },
            {
                'title':
                    "日期 : {error_date}\n".format(
                        error_date=datetime.now().strftime("%Y-%m-%d"))
                    + "时间 : {error_time}".format(
                        error_time=datetime.now().strftime("%H:%M:%S"))
            },
            {
                "title": warning_data['data']['task_name'] + " 运行异常"
            },
            {
                'title': '异常任务列表：\n' + node_list_content,
                'description': '点击查看详情'
            }
        ]

        warning_post_message = {
            "touser": "wangdp",
            "agentid": 2,
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        }

        warning_post_headers = {
            'content-type': 'application/json'
        }
        warning_post_data = json.dumps(warning_post_message, ensure_ascii=False).encode('utf8')

        result = requests.post(
            warning_post_url,
            data=warning_post_data,
            verify=False,
            headers=warning_post_headers,
            timeout=REQUEST_POST_TIME_OUT
        )
        print(result.json())

    def send_sms_node_task_message(self, message_data):
        auth = Auth(self.weixin_config['token'])
        weixin_access_token = auth.get_access_token()

        post_url = self.weixin_config['warn']['url'].format(
            weixin_access_token=weixin_access_token
        )
        articles = [
            {
                "title": "业务系统：SMS节点状态检查",
                "picurl": "http://wx2.sinaimg.cn/large/4afdac38ly1feqnewxygsj20hs08wt8u.jpg"
            },
            {
                "title": "{owner}/{repo}".format(
                    owner=message_data['data']['owner'],
                    repo=message_data['data']['repo']
                ),
                "description": message_data['data']['task_name']
            },
            {
                "title":
                    "日期 : {error_date}\n".format(
                        error_date=datetime.now().strftime("%Y-%m-%d"))
                    + "时间 : {error_time}".format(
                        error_time=datetime.now().strftime("%H:%M:%S"))
            },
            {
                "title": message_data['data']['task_name'] + " 运行正常"
            }
        ]

        post_message = {
            "touser": "wangdp",
            "agentid": 2,
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        }

        post_headers = {
            'content-type': 'application/json'
        }
        post_data = json.dumps(post_message, ensure_ascii=False).encode('utf8')

        result = requests.post(
            post_url,
            data=post_data,
            verify=False,
            headers=post_headers,
            timeout=REQUEST_POST_TIME_OUT
        )
        print(result.json())
