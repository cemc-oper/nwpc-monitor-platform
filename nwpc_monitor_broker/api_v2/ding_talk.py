# coding=utf-8
import requests
from .cache import save_dingtalk_access_token_to_cache, get_dingtalk_access_token_from_cache

class Auth(object):
    def __init__(self, config):
        self.corp_id = config['corp_id']
        self.corp_secret = config['corp_secret']
        self.url = config['url']

    def get_access_token_from_server(self):
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

    def get_access_token_from_cache(self):
        return get_dingtalk_access_token_from_cache()

    def save_access_token_to_cache(self, access_token):
        return save_dingtalk_access_token_to_cache(access_token)

    def get_access_token(self):
        dingtalk_access_token = get_dingtalk_access_token_from_cache()
        if dingtalk_access_token is None:
            self.get_access_token_from_server()
            dingtalk_access_token = get_dingtalk_access_token_from_cache()
        return dingtalk_access_token
