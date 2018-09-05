# coding=utf-8
from sqlalchemy import Column, Integer, String, Text, Index
from .model import Model
from .owner import Owner


class Repo(Model):
    __tablename__ = "repo"

    repo_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    repo_name = Column(String(45))
    repo_type = Column(String(10)) # [sms]
    repo_description = Column(Text())

    index_owner_repo = Index("index_owner_repo", owner_id, repo_name, unique=True)

    def __init__(self):
        Model.__init__(self)

    @staticmethod
    def query_repos_by_owner_name(session, owner_name:str):
        query = session.query(Repo).filter(Owner.owner_name == owner_name)\
            .filter(Owner.owner_id == Repo.owner_id)
        query_result = query.all()
        if query_result is None:
            query_owner_result = Owner.query_owner_by_owner_name(session, owner_name)
            if 'error' in query_owner_result:
                result = {
                    'error': "get owner error",
                    'data': {
                        'message': query_owner_result['error']
                    }
                }
            elif query_owner_result['data']['owner'] is None:
                result = {
                    'error': "owner doesn't exist.",
                    'data': {
                    }
                }
            else:
                result = {
                    'data': {
                        'repos': None
                    }
                }
            return result

        result = {
            'data': {
                'repos': query_result
            }
        }

        return result
