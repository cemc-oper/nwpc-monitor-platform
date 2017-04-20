# coding=utf-8
import datetime
import gzip

import requests
from flask import request, json, jsonify, url_for, session

from nwpc_monitor_web.app import app

from nwpc_monitor_web.app.api import api_app, weixin


@api_app.route("/user/info")
def get_uer_info():
    if 'user_info' in session:
        user_info = session['user_info']
        return jsonify({
            "status": "ok",
            "source": "session",
            "user_info": user_info
        })
    else:
        return jsonify({
            "status": "error"
        })