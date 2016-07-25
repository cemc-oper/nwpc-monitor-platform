# coding=utf-8

from flask import request, jsonify, json
import datetime
import requests

from nwpc_monitor_broker import app, db

from nwpc_monitor_broker.api_v2 import api_v2_app
from nwpc_monitor_broker.api_v2 import cache
from nwpc_monitor_broker.api_v2 import data_store

from nwpc_monitor.model import Repo, Owner, User, OrgUser, DingtalkUser, DingtalkWarnWatch

from sqlalchemy import and_, func


@api_v2_app.route('/orgs/<org>/repos')
def get_org_repos(org):
    query_repo_result = Repo.query_repos_by_owner_name(db.session, org)
    if 'error' in query_repo_result:
        result = {
            'app': 'nwpc_monitor_broker',
            'error': query_repo_result['error']
        }
        return jsonify(result)

    repos = []
    for an_repo in query_repo_result['data']['repos']:
        sms_server_status = cache.get_sms_server_status_from_cache(org, an_repo.repo_name, an_repo.repo_name)
        repos.append({
            'id': an_repo.repo_id,
            'name': an_repo.repo_name,
            'description': an_repo.repo_description,
            'update_time': sms_server_status['update_time']
        })

    result = {
        'data': {
            'repos': repos
        }
    }

    return jsonify(result)


@api_v2_app.route('/orgs/<org>/members')
def get_org_members(org):
    query_member_result = User.query_repo_members_by_org_name(db.session, org)
    if 'error' in query_member_result:
        result = {
            'app': 'nwpc_monitor_broker',
            'error': query_member_result['error']
        }
        return jsonify(result)

    members = []
    for an_member in query_member_result['data']['members']:
        members.append({
            'id': an_member.owner_id,
            'name': an_member.user_name
        })

    result = {
        'data': {
            'members': members
        }
    }

    return jsonify(result)


# warn

@api_v2_app.route('/orgs/<owner>/warning/dingtalk/watch/watchers/suggested')
def get_org_warning_watch_suggested_user(owner: str):
    """
    返回该组织的推荐关注用户列表
    :param owner:
    :return:

        正常情况
        {
            'data': {
                'owner': owner,
                'warning': {
                    'type': 'dingtalk',
                    'suggested_user_list': [
                        {
                            'owner_name': owner_name,
                            'is_watching': true or false,
                        },
                        ...
                    ]
                }
            }
        }

        出错
        {
            'error': error message
        }
    """
    repo_query = db.session.query(Owner, Repo). \
        filter(Owner.owner_name == owner). \
        filter(Owner.owner_id == Repo.owner_id)

    repo_query_result = repo_query.all()

    if len(repo_query_result) == 0:
        result = {
            'error': 'no repo for {owner}'.format(owner=owner)
        }
        return jsonify(result)

    repo_object_list = []
    (owner_object, repo_object) = repo_query_result[0]
    for (an_owner_object, a_repo_object) in repo_query_result:
        repo_object_list.append(a_repo_object)

    suggested_user_list = []

    if owner_object.owner_type == 'user':
        suggested_user_dingtalk_user_id_query = db.session.query(Owner.owner_name, DingtalkUser). \
            filter(DingtalkUser.user_id == owner_object.owner_id)
    elif owner_object.owner_type == 'org':
        suggested_user_dingtalk_user_id_query = db.session.query(Owner.owner_name, DingtalkUser). \
            filter(OrgUser.org_id == owner_object.owner_id). \
            filter(OrgUser.user_id == Owner.owner_id). \
            filter(DingtalkUser.user_id == Owner.owner_id)
    else:
        result = {
            'error': 'owner type {owner_type} is not supported'.format(owner_type=owner_object.owner_type)
        }
        return jsonify(result)

    suggested_user_query_result = suggested_user_dingtalk_user_id_query.all()
    for (an_user_name, a_dingtalk_user) in suggested_user_query_result:
        suggested_user_list.append({
            "owner_name": an_user_name,
            "is_watching": False,
            # "warn_watch":{
            #     "start_date_time": None,
            #     "end_date_time": None
            # }
        })

    result = {
        'data': {
            'owner': owner,
            'warning': {
                'type': 'dingtalk',
                'suggested_user_list': suggested_user_list
            }
        }
    }

    return jsonify(result)
