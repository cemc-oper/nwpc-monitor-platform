# coding=utf-8

from flask import request, jsonify

from nwpc_monitor_broker import app, db

from nwpc_monitor_broker.api_v2 import api_v2_app
from nwpc_monitor_broker.api_v2 import cache
from nwpc_monitor_broker.api_v2 import data_store

from nwpc_monitor.model import Repo, Owner, OrgUser, DingtalkUser, DingtalkWarnWatch

from sqlalchemy import and_


@api_v2_app.route('/repos/<owner>/<repo>/warning/dingtalk/watch/users')
def get_repo_warning_dingtalk_watch_users(owner:str, repo:str):
    """
    返回关注该项目的用户
    :param owner:
    :param repo:
    :return:

        正常情况
        {
            'data': {
                'owner': owner,
                'repo': repo,
                'warning': {
                    'type': 'dingtalk',
                    'watching_user_list': [
                        {
                            'owner_name': owner_object.owner_name,
                            'warn_watch': {
                                'start_date_time': ding_talk_warn_watch_object.start_date_time,
                                'end_date_time': ding_talk_warn_watch_object.end_date_time
                            }
                        },
                        ...
                    ]
                }
        }

        出错
        {
            'error': error message
        }
    """
    repo_query = db.session.query(Repo).filter(Owner.owner_name == owner).filter(Owner.owner_id == Repo.owner_id). \
        filter(Repo.repo_name == repo)

    repo_query_result = repo_query.all()

    if len(repo_query_result) == 0:
        result = {
            'error': 'no {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)
    elif len(repo_query_result) > 1:
        result = {
            'error': 'more than 1 {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)

    repo_object = repo_query_result[0]

    watch_user_query = db.session.query(Owner, DingtalkUser, DingtalkWarnWatch). \
        filter(DingtalkWarnWatch.repo_id == repo_object.repo_id). \
        filter(DingtalkWarnWatch.dingtalk_user_id == DingtalkUser.dingtalk_user_id). \
        filter(DingtalkUser.user_id == Owner.owner_id)
    watch_user_query_result = watch_user_query.all()

    user_list = []
    for (owner_object, ding_talk_user_object, ding_talk_warn_watch_object) in watch_user_query_result:
        an_user = {
            'owner_name': owner_object.owner_name,
            'warn_watch': {
                'start_date_time': ding_talk_warn_watch_object.start_date_time,
                'end_date_time': ding_talk_warn_watch_object.end_date_time
            }
        }
        user_list.append(an_user)

    result = {
        'data': {
            'owner': owner,
            'repo': repo,
            'warning': {
                'type': 'dingtalk',
                'watching_user_list': user_list
            }
        }
    }

    return jsonify(result)


@api_v2_app.route('/repos/<owner>/<repo>/warning/dingtalk/user/suggested')
def get_repo_warning_watch_suggested_user(owner:str, repo:str):
    """
    返回该项目的推荐关注用户列表
    :param owner:
    :param repo:
    :return:

        正常情况
        {
            'data': {
                'owner': owner,
                'repo': repo,
                'warning': {
                    'type': 'dingtalk',
                    'suggested_user_list': [
                        {
                            'owner_name': owner_name,
                            'is_watching': true or false

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
        filter(Owner.owner_id == Repo.owner_id). \
        filter(Repo.repo_name == repo)

    repo_query_result = repo_query.all()

    if len(repo_query_result) == 0:
        result = {
            'error': 'no repo: {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)
    elif len(repo_query_result) > 1:
        result = {
            'error': 'more than 1 {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)

    owner_object, repo_object = repo_query_result[0]

    suggested_user_list = []

    if owner_object.owner_type == 'user':
        suggested_user_dingtalk_user_id_query = db.session.query(Owner.owner_name, DingtalkUser.dingtalk_user_id). \
            filter(DingtalkUser.user_id == owner_object.owner_id). \
            subquery()
    elif owner_object.owner_type == 'org':
        suggested_user_dingtalk_user_id_query = db.session.query(Owner.owner_name, DingtalkUser.dingtalk_user_id). \
            filter(OrgUser.org_id == owner_object.owner_id). \
            filter(OrgUser.user_id == Owner.owner_id). \
            filter(DingtalkUser.user_id == Owner.owner_id).\
            subquery()
    else:
        result = {
            'error': 'owner type {owner_type} is not supported'.format(owner_type=owner_object.owner_type)
        }
        return jsonify(result)

    suggested_user_query = db.session.query(suggested_user_dingtalk_user_id_query.c.owner_name, DingtalkWarnWatch). \
        outerjoin(DingtalkWarnWatch,
                  and_(
                    DingtalkWarnWatch.dingtalk_user_id == suggested_user_dingtalk_user_id_query.c.dingtalk_user_id,
                    DingtalkWarnWatch.repo_id == repo_object.repo_id
                  )
        )

    suggested_user_query_result = suggested_user_query.all()
    for (an_user_name, a_dingtalk_user) in suggested_user_query_result:
        suggested_user_list.append({
            "owner_name": an_user_name,
            "is_watching": a_dingtalk_user and True or False
        })

    result = {
        'data': {
            'owner': owner,
            'repo': repo,
            'warning': {
                'type': 'dingtalk',
                'suggested_user_list': suggested_user_list
            }
        }
    }

    return jsonify(result)