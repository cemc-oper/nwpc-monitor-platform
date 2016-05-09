# coding=utf-8
from nwpc_monitor_broker import app

from flask import json, request, jsonify,render_template
import redis

redis_host = app.config['BROKER_CONFIG']['redis']['host']
redis_client = redis.Redis(host=redis_host)


@app.route('/')
def get_index_page():
    return render_template('index.html')