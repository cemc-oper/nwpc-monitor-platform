# coding=utf-8

from flask import request, jsonify
import datetime
import requests

from nwpc_monitor_broker import app, db

from nwpc_monitor_broker.api_v2 import api_v2_app
from nwpc_monitor_broker.api_v2 import cache
from nwpc_monitor_broker.api_v2 import data_store

from nwpc_monitor.model import Repo, Owner, User, DingtalkUser, DingtalkWarnWatch


@api_v2_app.route('/repos/<owner>/<repo>/warning/dingtalk/watch/users')
def get_repo_warning_dingtalk_watch_users(owner, repo):
    repo_query = db.session.query(Repo).filter(Owner.owner_name == owner).filter(Owner.owner_id == Repo.owner_id) \
        .filter(Repo.repo_name == repo)

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

    watch_user_query = db.session.query(Owner, DingtalkUser, DingtalkWarnWatch) \
        .filter(DingtalkWarnWatch.repo_id == repo_object.repo_id) \
        .filter(DingtalkWarnWatch.dingtalk_user_id == DingtalkUser.dingtalk_user_id) \
        .filter(DingtalkUser.user_id == Owner.owner_id)
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
                'watch_users': user_list
            }
        }
    }

    return jsonify(result)
