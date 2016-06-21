# coding=utf-8
from flask import Blueprint
from nwpc_monitor_broker import app

import redis

redis_host = app.config['BROKER_CONFIG']['redis']['host']['ip']
redis_port = app.config['BROKER_CONFIG']['redis']['host']['port']
redis_client = redis.Redis(host=redis_host, port=redis_port)

from pymongo import MongoClient
mongodb_client = MongoClient(app.config['BROKER_CONFIG']['mongodb']['host']['ip'],
                             app.config['BROKER_CONFIG']['mongodb']['host']['port'])

api_v2_app = Blueprint('api_v2_app', __name__, template_folder='template')

import nwpc_monitor_broker.api_v2.api_sms
import nwpc_monitor_broker.api_v2.api_org
import nwpc_monitor_broker.api_v2.api_repo