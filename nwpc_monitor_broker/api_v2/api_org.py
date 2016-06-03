# coding=utf-8

from flask import request, jsonify, json
import datetime
import requests

from nwpc_monitor_broker import app

from nwpc_monitor_broker.api_v2 import api_v2_app
from nwpc_monitor_broker.api_v2 import cache
from nwpc_monitor_broker.api_v2 import data_store


@api_v2_app.route('/orgs/<org>/repos')
def get_org_repos(org):
    return jsonify({
        'repos': [
            {'id': 1, 'name': 'nwpc_op'},
            {'id': 2, 'name': 'nwpc_qu'},
            {'id': 3, 'name': 'eps_nwpc_qu'},
        ]
    })

@api_v2_app.route('/orgs/<org>/members')
def get_org_members(org):
    return jsonify({
        'members': [
            {'id': 1, 'name': 'cuiyj'},
            {'id': 2, 'name': 'wangyt'},
            {'id': 3, 'name': 'wangyzh'},
            {'id': 4, 'name': 'wangdp'},
        ]
    })


