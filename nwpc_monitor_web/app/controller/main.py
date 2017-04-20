# coding=utf-8
from nwpc_monitor_web.app import app
from flask import render_template, request, session
from nwpc_monitor_web.app.api import weixin


@app.route('/')
@app.route('/about')
def get_index_page():
    code = request.args.get('code', None)
    if code is not None:
        weixin_client = weixin.WeixinApp(
            weixin_config=app.config['NWPC_MONITOR_WEB_CONFIG']['weixin_app']
        )
        user_info = weixin_client.get_user_info(code)
        if 'UserId' in user_info:
            session['user_info'] = user_info

    return render_template("app/welcome_app_index.html")
