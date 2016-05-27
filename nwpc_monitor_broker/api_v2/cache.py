import datetime
import json

from nwpc_monitor_broker.api_v2 import redis_client, mongodb_client

# mongodb

nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status

def get_sms_server_status_from_cache(owner: str, repo: str, sms_name: str) -> dict:

    key = {
        'owner': owner,
        'repo': repo,
        'sms_name': sms_name
    }

    result = sms_server_status.find_one(key)

    return result

def save_sms_server_status_to_cache(owner: str, repo: str, sms_name: str, message: dict) -> None:
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

# redis

access_token_key = "dingtalk_access_token"
def get_dingtalk_access_token_from_cache() -> str:
    dingtalk_access_token = redis_client.get(access_token_key)
    dingtalk_access_token = dingtalk_access_token.decode()
    return dingtalk_access_token

def save_dingtalk_access_token_to_cache(access_token: str) -> None:
    redis_client.set(access_token_key, access_token)
    return


def get_error_task_list_from_cache(owner: str, repo: str, sms_name: str)-> dict:
    error_task_key = "{owner}/{repo}/{sms_name}/task/error".format(owner=owner, repo=repo, sms_name=sms_name)
    cached_error_task_value = json.loads(redis_client.get(error_task_key))
    return cached_error_task_value

def save_error_task_list_to_cache(owner: str, repo: str, sms_name: str, error_task_value: dict)->None:
    error_task_key = "{owner}/{repo}/{sms_name}/task/error".format(owner=owner, repo=repo, sms_name=sms_name)
    redis_client.set(error_task_key, json.dumps(error_task_value))
    return
