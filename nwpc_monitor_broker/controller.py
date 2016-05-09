# coding=utf-8
from nwpc_monitor_broker import app

from flask import json, request, jsonify,render_template
import redis

REDIS_HOST = '10.28.32.175'
redis_client = redis.Redis(host=REDIS_HOST)


@app.route('/')
def get_index_page():
    return render_template('index.html')