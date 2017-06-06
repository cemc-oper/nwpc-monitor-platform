# coding=utf-8
from nwpc_monitor_web.app import app
from nwpc_monitor_web.app.common.weixin import Auth

auth = Auth(app.config['NWPC_MONITOR_WEB_CONFIG']['weixin_app']['token'])
weixin_access_token = auth.get_access_token_from_server()
