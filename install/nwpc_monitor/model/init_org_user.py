import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../../")
from nwpc_monitor.model import OrgUser


from .data import org_user_list
from .init_org import get_org
from .init_user import get_user

def create_org_user(org_id, user_id, relationship):
    org_user = OrgUser()
    org_user.org_id = org_id
    org_user.user_id = user_id
    org_user.relationship = relationship
    return org_user


def initial_org_user(session):
    org_users = []
    for a_record in org_user_list:
        org_name = a_record["org_name"]
        org = get_org(org_name, session)
        if org is None:
            continue

        users = a_record["users"]
        for an_user in users:
            user_name = an_user["user_name"]
            relationship = an_user["relationship"]
            user = get_user(user_name, session)
            if user is None:
                continue
            org_users.append(create_org_user(org.owner_id, user.owner_id, relationship))

    for org_user in org_users:
        session.add(org_user)

    session.commit()


def get_org_user(org_id, user_id, session):
    query = session.query(OrgUser).filter(OrgUser.org_id==org_id).filter(OrgUser.user_id==user_id)
    org_user = query.first()
    return org_user


def remove_org_user(session):
    org_users = []
    for a_record in org_user_list:
        org_name = a_record["org_name"]
        org = get_org(org_name, session)
        if org is None:
            continue

        users = a_record["users"]
        for an_user in users:
            user_name = an_user["user_name"]
            relationship = an_user["relationship"]
            user = get_user(user_name, session)
            if user is None:
                continue
            org_user = get_org_user(org.owner_id, user.owner_id, session)
            if org_user is None:
                continue
            org_users.append(org_user)

    for org_user in org_users:
        session.delete(org_user)

    session.commit()