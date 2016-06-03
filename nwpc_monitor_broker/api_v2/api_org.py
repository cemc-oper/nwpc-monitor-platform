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
    return jsonify([
        {'id': 1, 'name': 'nwpc_op'},
        {'id': 2, 'name': 'nwpc_qu'},
        {'id': 3, 'name': 'eps_nwpc_qu'},
    ])



