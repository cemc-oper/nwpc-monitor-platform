# coding=utf-8
from sqlalchemy import Column, Integer, String
from .model import Model

class Owner(Model):
    __tablename__ = "owner"

    owner_id = Column(Integer(), primary_key=True)
    owner_name = Column(String(45))
    owner_type = Column(String(10)) # [user, org]

    def __init__(self):
        Model.__init__(self)

    @staticmethod
    def query_owner_by_owner_name(session, owner_name:str):
        query = session.query(Owner).filter(Owner.owner_name == owner_name)
        query_result = query.all()
        if len(query_result) >=1:
            result = {
                'error': 'we have more than one owner with a single name, please contact admin.',
                'message': '',
                'data':{

                }
            }
            return result

        if query_result is None:
            result = {
                'data': {
                    'owner': None
                }
            }
            return result
        owner = query_result.first()
        result = {
            'data': {
                'owner': owner
            }
        }
        return result
