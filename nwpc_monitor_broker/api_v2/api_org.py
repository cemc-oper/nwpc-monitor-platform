# coding=utf-8

from flask import request, jsonify, json
import datetime
import requests

from nwpc_monitor_broker import app, db

from nwpc_monitor_broker.api_v2 import api_v2_app
from nwpc_monitor_broker.api_v2 import cache
from nwpc_monitor_broker.api_v2 import data_store

from nwpc_monitor.model import Repo, User


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
        repos.append({
            'id': an_repo.repo_id,
            'name': an_repo.repo_name
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


