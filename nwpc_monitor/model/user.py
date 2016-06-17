# coding=utf-8
from sqlalchemy import Column, Integer, String, Text
from .model import Model
from .org import Org
from .org_user import OrgUser

class User(Model):
    __tablename__ = "user"

    owner_id = Column(Integer(), primary_key=True)
    user_name = Column(String(45))
    user_description = Column(Text())

    def __init__(self):
        Model.__init__(self)

    @staticmethod
    def query_repo_members_by_org_name(session, org_name):
        query = session.query(User).filter(Org.org_name == org_name)\
            .filter(Org.owner_id == OrgUser.org_id)\
            .filter(OrgUser.user_id == User.owner_id)

        query_result = query.all()

        if query_result is None:
            query_org_result = Org.query_org_by_org_name(session, org_name)
            if 'error' in query_org_result:
                result = {
                    'error': "get org error",
                    'data': {
                        'message': query_org_result['error']
                    }
                }
            elif query_org_result['data']['member'] is None:
                result = {
                    'error': "org doesn't exist.",
                    'data': {
                    }
                }
            else:
                result = {
                    'data': {
                        'members': None
                    }
                }
            return result

        result = {
            'data': {
                'members': query_result
            }
        }

        return result