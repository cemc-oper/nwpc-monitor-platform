# coding=utf-8
from flask import render_template, request

from nwpc_monitor_web.app import app
from nwpc_monitor_web.app.util.user import get_user_info


@app.route('/')
@app.route('/about')
def get_index_page():
    code = request.args.get('code', None)
    get_user_info(code)

    return render_template("app/welcome_app_index.html")
