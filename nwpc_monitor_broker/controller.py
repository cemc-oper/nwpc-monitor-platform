# coding=utf-8
from nwpc_monitor_broker import app

from flask import json, request, jsonify,render_template
import redis

redis_host = app.config['BROKER_CONFIG']['redis']['host']['ip']
redis_port = app.config['BROKER_CONFIG']['redis']['host']['port']
redis_client = redis.Redis(host=redis_host, port=redis_port)


@app.route('/')
def get_index_page():
    return render_template('index.html')