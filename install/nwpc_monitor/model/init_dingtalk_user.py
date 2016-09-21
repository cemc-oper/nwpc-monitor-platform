import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../../")
from nwpc_monitor.model import User, DingtalkUser

from .data import dingtalk_user_list
from .init_user import get_user



def create_dingtalk_user(user_id, dingtalk_member_userid):
    dingtalk_user = DingtalkUser()
    dingtalk_user.user_id = user_id
    dingtalk_user.dingtalk_member_userid = dingtalk_member_userid
    return dingtalk_user


def init_dingtalk_users(session):
    dingtalk_users = []
    for a_record in dingtalk_user_list:
        user_name = a_record["user_name"]
        dingtalk_member_userid = a_record["dingtalk_member_userid"]

        user = get_user(user_name, session)
        if user is None:
            continue

        dingtalk_users.append(create_dingtalk_user(user.owner_id, dingtalk_member_userid))

    for dingtalk_user in dingtalk_users:
        session.add(dingtalk_user)
    session.commit()


def get_dingtalk_user(user_id, session):
    query = session.query(DingtalkUser).filter(DingtalkUser.user_id == user_id)
    dingtalk_user = query.first()
    return dingtalk_user


def remove_dingtalk_users(session):
    dingtalk_users = []
    for a_record in dingtalk_user_list:
        user_name = a_record["user_name"]

        user = get_user(user_name, session)
        if user is None:
            continue

        dingtalk_user = get_dingtalk_user(user.owner_id, session)
        if dingtalk_user is None:
            continue
        dingtalk_users.append(dingtalk_user)

    for dingtalk_user in dingtalk_users:
        session.delete(dingtalk_user)
    session.commit()