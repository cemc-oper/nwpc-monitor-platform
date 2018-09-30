# coding: utf-8
import datetime
from nmp_broker.common.data_store.rmdb import get_new_64bit_ticket


def save_abnormal_jobs_to_nmp_model_system(
        owner: str, repo: str,
        plugin_result: dict
) -> dict:
    from nmp_model.mongodb.blobs.workload.abnormal_jobs import (
        AbnormalJobsContent, AbnormalJobsBlobData, AbnormalJobsBlob)
    from nmp_model.mongodb.trees.workload_tree_node import WorkloadTreeNode
    from nmp_model.mongodb.tree import TreeData, Tree
    from nmp_model.mongodb.commits.workload_commit import WorkloadCommit, WorkloadCommitData

    abnormal_jobs_blob = AbnormalJobsBlob(
        owner=owner,
        repo=repo,
        ticket_id=get_new_64bit_ticket(),
        data=AbnormalJobsBlobData(
            workload_system=plugin_result['data']['workload_system'],
            user_name=plugin_result['data']['user_name'],
            collected_time=plugin_result['data']['collected_time'],
            content=AbnormalJobsContent(
                plugins=plugin_result['data']['plugins'],
                abnormal_jobs=plugin_result['data']['target_job_items']
            )
        )
    )

    abnormal_jobs_blob.save()

    tree_object = Tree(
        ticket_id=get_new_64bit_ticket(),
        owner=owner,
        repo=repo,
        data=TreeData(
            nodes=[
                WorkloadTreeNode(
                    type='abnormal_jobs',
                    name='loadleveler.abnormal_jobs',
                    blob_ticket_id=abnormal_jobs_blob.ticket_id
                )
            ]
        )
    )

    tree_object.save()

    commit_object = WorkloadCommit(
        ticket_id=get_new_64bit_ticket(),
        owner=owner,
        repo=repo,
        data=WorkloadCommitData(
            committer='nmp-broker',
            type='abnormal_jobs',
            tree_ticket_id=tree_object.ticket_id,
            committed_time=datetime.datetime.utcnow()
        )
    )

    commit_object.save()

    return {
        'blobs': [
            abnormal_jobs_blob
        ],
        'trees': [
            tree_object
        ],
        'commits': [
            commit_object
        ]
    }


# loadleveler status

def save_hpc_loadleveler_status_to_cache(user: str, message: dict) -> tuple:
    key = {
        'data.user': user
    }
    value = {
        'app': 'nmp_broker',
        'event': 'post_sms_task_check',
        'data': {
            'user': user,
            'type': 'job_list',
            'update_time': datetime.datetime.utcnow(),
            'message': message
        }

    }
    hpc_loadleveler_status.update(key, value, upsert=True)
    return key, value


def get_hpc_loadleveler_status_from_cache(user: str) -> dict:
    key = {
        'owner': user
    }
    value = hpc_loadleveler_status.find_one(key, {"_id": 0})
    return value