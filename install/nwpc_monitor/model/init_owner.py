import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../../")
from nwpc_monitor.model import Owner

from .data import owner_list

def create_owner(owner_name, owner_type):
    owner = Owner()
    owner.owner_name = owner_name
    owner.owner_type = owner_type
    return owner


def initial_owners(session):
    owners = [ create_owner(an_owner["owner_name"], an_owner["owner_type"])
               for an_owner in owner_list ]

    for owner in owners:
        session.add(owner)

    session.commit()


def get_owner(owner_name, owner_type, session):
    query = session.query(Owner).filter(Owner.owner_name==owner_name).filter(Owner.owner_type==owner_type)
    owner = query.first()
    return owner


def remove_owners(session):
    owners = [ get_owner(an_owner["owner_name"], an_owner["owner_type"], session)
               for an_owner in owner_list]

    for owner in owners:
        if owner is not None:
            session.delete(owner)
    session.commit()