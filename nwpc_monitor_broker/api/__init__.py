# coding=utf-8
from flask import Blueprint
from nwpc_monitor_broker import app

import redis

redis_host = app.config['BROKER_CONFIG']['redis']['host']
redis_client = redis.Redis(host=redis_host)

api_app = Blueprint('api_app', __name__, template_folder='template')

import api_sms