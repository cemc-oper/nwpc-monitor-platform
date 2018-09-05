# coding=utf-8
from sqlalchemy import Column, Integer, String, Text, Index, ForeignKey
from .model import Model
from .owner import Owner


class Org(Model):
    __tablename__ = "org"

    owner_id = Column(Integer, ForeignKey(Owner.owner_id), primary_key=True)
    org_name = Column(String(45), nullable=False)
    org_description = Column(Text)

    index_org_name = Index('index_org_name', org_name, unique=True)

    def __init__(self):
        Model.__init__(self)

    @staticmethod
    def query_owner_by_owner_name(session, org_name:str):
        query = session.query(Org).filter(Org.org_name == org_name)
        query_result = query.all()
        if len(query_result) >=1:
            result = {
                'error': 'we have more than one org with a single name, please contact admin.',
                'message': '',
                'data':{

                }
            }
            return result

        if len(query_result) == 0 or query_result is None:
            result = {
                'data': {
                    'org': None
                }
            }
            return result
        org = query_result.first()
        result = {
            'data': {
                'org': org
            }
        }
        return result
