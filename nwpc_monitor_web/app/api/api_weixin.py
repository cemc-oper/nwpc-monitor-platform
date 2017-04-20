# coding=utf-8

from flask import jsonify, session

from nwpc_monitor_web.app.api import api_app


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