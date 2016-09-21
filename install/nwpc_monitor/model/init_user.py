import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../../")
from nwpc_monitor.model import User


from .data import owner_list
from .init_owner import get_owner

def create_user(owner_id, user_name):
    user = User()
    user.owner_id = owner_id
    user.user_name = user_name
    return user


def initial_users(session):
    users = []
    for an_owner in owner_list:
        if an_owner["owner_type"] == "user":
            owner = get_owner(an_owner["owner_name"], an_owner["owner_type"], session)
            if owner is None:
                continue
            users.append(create_user(owner.owner_id, an_owner["owner_name"]))

    for user in users:
        session.add(user)

    session.commit()


def get_user(org_name, session):
    query = session.query(User).filter(User.user_name==org_name)
    user = query.first()
    return user


def remove_users(session):
    users = []
    for an_owner in owner_list:
        if an_owner["owner_type"] == "user":
            users.append(get_user(an_owner["owner_name"], session))

    for user in users:
        if user is not None:
            session.delete(user)
    session.commit()