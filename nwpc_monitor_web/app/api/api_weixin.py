# coding=utf-8
import datetime
import gzip

import requests
from flask import request, json, jsonify, url_for

from nwpc_monitor_web.app import app

from nwpc_monitor_web.app.api import api_app, weixin


@api_app.route("/user/info")
def get_uer_info():
    code = request.args.get('code', None)
    if code is None:
        return jsonify({
            "status": "error"
        })
    weixin_client = weixin.WeixinApp(
        weixin_config=app.config['NWPC_MONITOR_WEB_CONFIG']['weixin_app']
    )
    user_info = weixin_client.get_user_info(code)
    print(user_info)
    return jsonify({
        "status": "ok",
        "user_info": user_info,
        "access_token": weixin_client.auth.get_access_token()
    })
