import datetime
from flask import json

from nwpc_monitor_broker.api_v2 import redis_client, mongodb_client

from nwpc_monitor.model.nwpc_takler import Commit, Tree, Blob, Ref

from .data_store import get_new_64bit_ticket

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


def save_sms_server_status_to_nwpc_takler_object_system(
        owner: str, repo: str, sms_name: str,
        message: dict,
        error_task_dict_list: list
) -> int:
    status_blob = Blob()
    status_blob.id = get_new_64bit_ticket()
    status_blob.owner = owner
    status_blob.repo = repo
    status_blob_data = {
        'type': 'status',
        'name': 'sms_server_status',
        'content': {
            'sms_name': sms_name,
            'update_time': datetime.datetime.now(),
            'collected_time': message['time'],
            'status': message['status']
        }
    }
    status_blob.set_data(status_blob_data)
    blobs_collection = nwpc_monitor_platform_mongodb.blobs
    blobs_collection.insert_one(status_blob.to_dict())

    aborted_tasks_blob = Blob()
    aborted_tasks_blob.id = get_new_64bit_ticket()
    aborted_tasks_blob.owner = owner
    aborted_tasks_blob.repo = repo
    aborted_tasks_blob_data = {
        'type': 'aborted_tasks',
        'name': 'sms_server_aborted_tasks',
        'content': {
            'status_blob_id': status_blob.id,
            'sms_name': sms_name,
            'update_time': datetime.datetime.now(),
            'collected_time': message['time'],
            'tasks': error_task_dict_list
        }
    }
    aborted_tasks_blob.set_data(aborted_tasks_blob_data)
    blobs_collection.insert_one(aborted_tasks_blob.to_dict())

    tree_object = Tree()
    tree_object.id = get_new_64bit_ticket()
    tree_object.owner = owner
    tree_object.repo = repo
    tree_object_data = {
        'nodes': [
            {
                'type': 'status',
                'name': 'sms_server_status',
                'blob_id': status_blob.id
            },
            {
                'type': 'aborted_tasks',
                'name': 'sms_server_aborted_tasks',
                'blob_id': aborted_tasks_blob.id
            }
        ]
    }
    tree_object.set_data(tree_object_data)
    trees_collection = nwpc_monitor_platform_mongodb.trees
    trees_collection.insert_one(tree_object.to_dict())

    commit_object = Commit()
    commit_object.id = get_new_64bit_ticket()
    commit_object.owner = owner
    commit_object.repo = repo
    commit_object_data = {
        'committer': 'aix',
        'type': 'status',
        'tree_id': tree_object.id,
        'committed_time': datetime.datetime.now()
    }
    commit_object.set_data(commit_object_data)
    commits_collection = nwpc_monitor_platform_mongodb.commits
    commits_collection.insert_one(commit_object.to_dict())

    # NOTE:
    #   如果只保存出错时的任务，Ref就失去意义

    # # find ref in mongodb
    # ref_collection = nwpc_monitor_platform_mongodb.refs
    #
    # ref_key = {
    #     'owner': owner,
    #     'repo': repo,
    #     'data.key': 'sms_server/status/head'
    # }
    # ref_found_result = ref_collection.find_one(ref_key)
    # if ref_found_result is None:
    #     ref_object = Ref()
    #     ref_object.id = get_new_64bit_ticket()
    #     ref_object.owner = owner
    #     ref_object.repo = repo
    #     ref_object_data = {
    #         'key': 'sms_server/status/head',
    #         'type': 'blob',
    #         'id': status_blob.id
    #     }
    #     ref_object.set_data(ref_object_data)
    #     # save
    #     ref_collection.update(ref_key, ref_object.to_dict(), upsert=True)
    # else:
    #     ref_found_result['data']['id'] = status_blob.id
    #     ref_found_result['timestamp'] = datetime.datetime.now()
    #     # save
    #     ref_collection.update(ref_key, ref_found_result, upsert=True)
    return commit_object.id


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


def get_weixin_access_token_from_cache() -> str:
    weixin_access_token = redis_client.get(weixin_access_token_key)
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
