# coding=utf-8
from flask import session
from nwpc_monitor_web.app import app
from nwpc_monitor_web.app.util import weixin


class UserType:
    Member = 'member'
    Visitor = 'visitor'
    Anonymous = 'anonymous'


def get_user_type():
    if 'user_info' in session:
        user_info = session['user_info']
        if 'UserId' in user_info:
            return UserType.Member
        elif 'OpenId' in user_info:
            return UserType.Visitor
    return UserType.Anonymous


def get_user_info(code):
    if code is None:
        return None
    weixin_client = weixin.WeixinApp(
        weixin_config=app.config['NWPC_MONITOR_WEB_CONFIG']['weixin_app']
    )
    user_info = weixin_client.get_user_info(code)
    if 'errcode' not in user_info:
        session['user_info'] = user_info