import datetime
from flask import json

from nwpc_monitor_broker.api_v2 import redis_client, mongodb_client

# mongodb

nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status
hpc_disk_usage_status = nwpc_monitor_platform_mongodb.hpc_disk_usage_status
hpc_disk_space_status = nwpc_monitor_platform_mongodb.hpc_disk_space_status
hpc_loadleveler_status = nwpc_monitor_platform_mongodb.hpc_loadleveler_status


# sms
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

# hpc
# disk usage


def get_hpc_disk_usage_status_from_cache(user: str) -> dict:
    key = {
        'user': user
    }
    result = hpc_disk_usage_status.find_one(key, {"_id": 0})
    return result


def save_hpc_disk_usage_status_to_cache(user: str, message: dict) -> tuple:
    key = {
        'user': user
    }
    value = {
        'user': user,
        'update_time': datetime.datetime.now(),
        'message': message
    }
    hpc_disk_usage_status.update(key, value, upsert=True)
    return key, value


# disk space

def get_hpc_disk_space_status_from_cache() -> dict:
    key = {
        'user': 'hpc'
    }
    result = hpc_disk_space_status.find_one(key, {"_id": 0})
    return result


def save_hpc_disk_space_status_to_cache(message:str) -> tuple:
    key = {
        'user': 'hpc'
    }
    value = {
        'user': 'hpc',
        'update_time': datetime.datetime.now(),
        'message': message
    }
    hpc_disk_space_status.update(key, value, upsert=True)
    return key, value


# loadleveler status

def save_hpc_loadleveler_status_to_cache(user: str, message: dict) -> tuple:
    key = {
        'user': user
    }
    value = {
        'user': user,
        'update_time': datetime.datetime.now(),
        'message': message
    }
    hpc_loadleveler_status.update(key, value, upsert=True)
    return key, value


def get_hpc_loadleveler_status_from_cache(user: str) -> dict:
    key = {
        'user': user
    }
    value = hpc_loadleveler_status.find_one(key, {"_id": 0})
    return value


# redis
dingtalk_access_token_key = "dingtalk_access_token"


def get_dingtalk_access_token_from_cache() -> str:
    dingtalk_access_token = redis_client.get(dingtalk_access_token_key)
    dingtalk_access_token = dingtalk_access_token.decode()
    return dingtalk_access_token


def save_dingtalk_access_token_to_cache(access_token: str) -> None:
    redis_client.set(dingtalk_access_token_key, access_token)
    return

weixin_access_token_key = "weixin_access_token"


def get_weixin_access_token_from_cache() -> str or None:
    weixin_access_token = redis_client.get(weixin_access_token_key)
    if weixin_access_token is None:
        return None
    weixin_access_token = weixin_access_token.decode()
    return weixin_access_token


def save_weixin_access_token_to_cache(access_token: str) -> None:
    redis_client.set(weixin_access_token_key, access_token)
    return


def get_error_task_list_from_cache(owner: str, repo: str)-> dict:
    error_task_key = "{owner}/{repo}/sms/task/error".format(owner=owner, repo=repo)
    cached_error_task_value = json.loads(redis_client.get(error_task_key).decode())
    return cached_error_task_value


def save_error_task_list_to_cache(owner: str, repo: str, error_task_value: dict)->None:
    error_task_key = "{owner}/{repo}/sms/task/error".format(owner=owner, repo=repo)
    redis_client.set(error_task_key, json.dumps(error_task_value))
    return
