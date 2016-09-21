import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../../")
from nwpc_monitor.model import Org


from .data import owner_list
from .init_owner import get_owner

def create_org(owner_id, org_name):
    org = Org()
    org.owner_id = owner_id
    org.org_name = org_name
    return org


def initial_orgs(session):
    orgs = []
    for an_owner in owner_list:
        if an_owner["owner_type"] == "org":
            owner = get_owner(an_owner["owner_name"], an_owner["owner_type"], session)
            if owner is None:
                continue
            orgs.append(create_org(owner.owner_id, an_owner["owner_name"]))

    for org in orgs:
        session.add(org)

    session.commit()


def get_org(org_name, session):
    query = session.query(Org).filter(Org.org_name==org_name)
    org = query.first()
    return org


def remove_orgs(session):
    orgs = []
    for an_owner in owner_list:
        if an_owner["owner_type"] == "org":
            orgs.append(get_org(an_owner["owner_name"], session))

    for org in orgs:
        if org is not None:
            session.delete(org)
    session.commit()